import datetime
import sys
import uuid
import os
import csv

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from DataBaseService.main import dataBaseController


from GoogleAdsService import Enum

_DATE_FORMAT = "%Y%m%d"
_DEFAULT_PAGE_SIZE = 1000


# fetching token details from database
db = dataBaseController
client_id = '1040281022647-soclnfbgmiujemuojhbopomnkf0o1724.apps.googleusercontent.com'
login_customer_id = '2838771052'

token_details = db.get_GoogleAds_Token(client_id, login_customer_id)

developer_token = token_details['developer_token']
client_secret = token_details['client_secret']
refresh_token = token_details['refresh_token']

token_dict = {"developer_token": developer_token, "refresh_token": refresh_token, "client_id": client_id,
              "client_secret": client_secret, "login_customer_id": login_customer_id, "use_proto_plus": True}


# This interface allows the user to create and manage all the marketing fields,
# using Google Ads APIs.
client = GoogleAdsClient.load_from_dict(token_dict, version="v10")


# This interface allows the user to create and manage all the marketing fields,
# using Google Ads APIs.
# dir_path = os.path.dirname(os.path.realpath(__file__))
# curr_path = dir_path + "\google-ads.yaml"
# client = GoogleAdsClient.load_from_storage(path=curr_path, version="v10")


# creates a new campaign
def create_new_campaign(customer_id, budget, name, days_to_start, weeks_to_end, status, delivery_method, period,
                        advertising_channel_type, payment_mode,
                        targeting_locations, targeting_gender, targeting_device_type, targeting_min_age,
                        targeting_max_age, targeting_interest
                        ):
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")

    # Create a budget
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Interplanetary Budget {uuid.uuid4()}"
    if delivery_method == "STANDARD" or delivery_method is None or delivery_method == "":
        campaign_budget.delivery_method = client.get_type(
            "BudgetDeliveryMethodEnum").BudgetDeliveryMethod.STANDARD
    elif delivery_method == "ACCELERATED":
        campaign_budget.delivery_method = client.get_type(
            "BudgetDeliveryMethodEnum").BudgetDeliveryMethod.ACCELERATED
    campaign_budget.amount_micros = 1000000 * budget
    if period == "DAILY" or period is None or period == "":
        campaign_budget.period = client.get_type(
                "BudgetPeriodEnum").BudgetPeriod.DAILY
    elif period == "CUSTOM_PERIOD":
        campaign_budget.period = client.get_type(
            "BudgetPeriodEnum").BudgetPeriod.CUSTOM_PERIOD

    # Add budget.
    try:
        campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[campaign_budget_operation]
        )
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)
        # [END add_campaigns]

    # Create campaign.
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = name

    # todo not working more types
    campaign.advertising_channel_type = client.get_type("AdvertisingChannelTypeEnum").AdvertisingChannelType.SEARCH

    if payment_mode in Enum.Payments.keys():
        campaign.payment_mode = Enum.Payments[payment_mode]()
    # todo check if working
    elif payment_mode == "" or payment_mode is None:
        campaign.payment_mode = client.get_type("PaymentModeEnum").PaymentMode.CLICKS

    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    if status == "PAUSED":
        campaign.status = client.get_type("CampaignStatusEnum").CampaignStatus.PAUSED
    elif status == "ENABLED":
        campaign.status = client.get_type("CampaignStatusEnum").CampaignStatus.ENABLED

    # Set the bidding strategy and budget.
    campaign.manual_cpc.enhanced_cpc_enabled = True
    campaign.campaign_budget = campaign_budget_response.results[0].resource_name

    # Set the campaign network options.
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_content_network = False
    campaign.network_settings.target_partner_search_network = False

    # Optional: Set the start date.
    start_time = datetime.date.today() + datetime.timedelta(days=days_to_start)
    campaign.start_date = datetime.date.strftime(start_time, _DATE_FORMAT)

    # Optional: Set the end date.
    end_time = start_time + datetime.timedelta(weeks=weeks_to_end)
    campaign.end_date = datetime.date.strftime(end_time, _DATE_FORMAT)

    # Add the campaign.
    try:
        campaign_response = campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[campaign_operation])
        campaign_id = campaign_response.results[0].resource_name.split("/")[3]

        # Add the targeting
        campaign_criterion_service = client.get_service("CampaignCriterionService")

        operations = [
            _create_location_op(customer_id, campaign_id, targeting_locations),
            _create_age_op(customer_id, campaign_id, targeting_min_age, targeting_max_age),
            _create_gender_op(customer_id, campaign_id, targeting_gender),
            _create_device_op(customer_id, campaign_id, targeting_device_type),
            _create_user_interest_op(customer_id, campaign_id, targeting_interest),
        ]

        campaign_criterion_response = campaign_criterion_service.mutate_campaign_criteria(
            customer_id=customer_id, operations=operations
        )

        for result in campaign_criterion_response.results:
            print(f'Added campaign criterion "{result.resource_name}".')

        return {"status": 200, "body": {"id": campaign_id}}
    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


# returns all campaign belongs to AD_ACCOUNT_ID
def get_all_campaigns(customer_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
            SELECT
              campaign.id,
              campaign.campaign_budget,
              campaign.name,
              campaign.start_date,
              campaign.end_date,
              campaign.status,
              campaign.advertising_channel_type,
              campaign.payment_mode
            FROM campaign
            WHERE campaign.status != \"REMOVED\"
            ORDER BY campaign.id"""

    # Issues a search request using streaming.
    try:
        response = ga_service.search_stream(customer_id=customer_id, query=query)

        campaigns = []
        for batch in response:
            for row in batch.results:
                campaigns.append((row.campaign.id,row.campaign.name,row.campaign.advertising_channel_type))
                # print(f"Campaign with ID {row.campaign.id} and name "
                #       f'"{row.campaign.name}" was found.')
        return {"status": 200, "body": {"campaigns": {"data":campaigns}}} #todo add id_act?

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


# returns a campaign by id
def get_campaign_by_id(customer_id, campaign_id):
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
                SELECT
                  campaign.id,
                  campaign.name
                FROM campaign
                WHERE campaign.id = "{campaign_id}"
                ORDER BY campaign.id"""

    # Issues a search request using streaming.
    try:
        response = ga_service.search_stream(customer_id=customer_id, query=query)

        campaigns = []
        for batch in response:
            for row in batch.results:
                campaigns.append((row.campaign.id, row.campaign.name))
        return {"status": 200, "body":{"campaigns":  {"data":campaigns}}}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


# deletes a campaign
def delete_campaign(customer_id, campaign_id):
    campaign_service = client.get_service("CampaignService")
    campaign_operation = client.get_type("CampaignOperation")

    resource_name = campaign_service.campaign_path(customer_id, campaign_id)
    campaign_operation.remove = resource_name

    try:
        campaign_response = campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[campaign_operation]
        )

        campaign_id = campaign_response.results[0].resource_name.split("/")[3]
        # print(f"Removed campaign {campaign_response.results[0].resource_name}.")
        return {"status": 200, "data": {"id": campaign_id}}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


# creates a new ad group
def create_new_ad_group(customer_id, campaign_id, name, status, cpc_bid):
    ad_group_service = client.get_service("AdGroupService")
    campaign_service = client.get_service("CampaignService")

    # Create ad group.
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = name
    if status == "PAUSED":
        ad_group.status = client.get_type("AdGroupStatusEnum").AdGroupStatus.PAUSED
    elif status == "ENABLED":
        ad_group.status = client.get_type("AdGroupStatusEnum").AdGroupStatus.ENABLED
    ad_group.campaign = campaign_service.campaign_path(customer_id, campaign_id)
    ad_group.type_ = client.get_type(
        "AdGroupTypeEnum"
    ).AdGroupType.SEARCH_STANDARD
    ad_group.cpc_bid_micros = cpc_bid * 1000000

    # Add the ad group.
    try:
        ad_group_response = ad_group_service.mutate_ad_groups(
            customer_id=customer_id, operations=[ad_group_operation])

        ad_group_id = ad_group_response.results[0].resource_name.split("/")[3]
        return {"status": 200, "body": {"ad_group_id": ad_group_id} }

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


# returns all ad groups belongs to campaign_id
def get_all_ad_groups(customer_id, campaign_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
            SELECT
              campaign.id,
              ad_group.id,
              ad_group.name
            FROM ad_group
            WHERE ad_group.status != \"REMOVED\"
            """

    if campaign_id:
        query += f"AND campaign.id = {campaign_id}"

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = _DEFAULT_PAGE_SIZE

    try:
        results = ga_service.search(request=search_request)

        ad_groups = []
        for row in results:
            ad_groups.append((row.ad_group.id, row.ad_group.name))
        return {"status": 200, "body": ad_groups}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)

# returns a campaign by id
def get_ad_group_by_id(customer_id, ad_group_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
                SELECT
                  ad_group.id,
                  ad_group.name
                FROM ad_group
                """

    if ad_group_id:
        query += f" WHERE ad_group.id = {ad_group_id}"

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = _DEFAULT_PAGE_SIZE

    try:
        results = ga_service.search(request=search_request)

        ad_groups = []
        for row in results:
            ad_groups.append((row.ad_group.id, row.ad_group.name))
        return {"status": 200, "body": ad_groups}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)

# deletes an ad group
def delete_ad_group(customer_id, ad_group_id):
    ad_group_service = client.get_service("AdGroupService")
    ad_group_operation = client.get_type("AdGroupOperation")

    resource_name = ad_group_service.ad_group_path(customer_id, ad_group_id)
    ad_group_operation.remove = resource_name

    try:
        ad_group_response = ad_group_service.mutate_ad_groups(
            customer_id=customer_id, operations=[ad_group_operation]
        )

        # print(f"Removed ad group {ad_group_response.results[0].resource_name}.")
        ad_group_id = ad_group_response.results[0].resource_name.split("/")[3]
        return {"status": 200, "data": {"ad_group_id":ad_group_id}}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


# adds a keyword to an ad group
def add_keyword(customer_id, ad_group_id, keyword_text):
    ad_group_service = client.get_service("AdGroupService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    # Create keyword.
    ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id)
    ad_group_criterion.status = client.get_type(
        "AdGroupCriterionStatusEnum").AdGroupCriterionStatus.ENABLED
    ad_group_criterion.keyword.text = keyword_text
    ad_group_criterion.keyword.match_type = client.get_type(
        "KeywordMatchTypeEnum").KeywordMatchType.EXACT

    # Optional field
    # All fields can be referenced from the protos directly.
    # The protos are located in subdirectories under:
    # https://github.com/googleapis/googleapis/tree/master/google/ads/googleads
    # ad_group_criterion.negative = True

    # Optional repeated field
    # ad_group_criterion.final_urls.append('https://www.example.com')

    # Add keyword
    try:
        ad_group_criterion_response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=[ad_group_criterion_operation],
        )

        keyword_id = ad_group_criterion_response.results[0].resource_name.split("/")[3].split("~")[1]
        return {"status": 200, "body":{"keyword_text": keyword_text, "keyword_id": keyword_id}}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


# gets the keywords of an ad group
def get_keywords(customer_id, ad_group_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
            SELECT
              ad_group.id,
              ad_group.status,
              ad_group_criterion.type,
              ad_group_criterion.criterion_id,
              ad_group_criterion.keyword.text,
              ad_group_criterion.status,
              ad_group_criterion.keyword.match_type
            FROM ad_group_criterion
            WHERE ad_group_criterion.type = KEYWORD
            AND ad_group.status = 'ENABLED'
            AND ad_group_criterion.status IN ('ENABLED', 'PAUSED')
            """


    if ad_group_id:
        query += f" AND ad_group.id = {ad_group_id}"

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = _DEFAULT_PAGE_SIZE

    try:
        results = ga_service.search(request=search_request)

        keywords = []
        for row in results:
            ad_group = row.ad_group
            ad_group_criterion = row.ad_group_criterion
            keyword = row.ad_group_criterion.keyword

            keywords.append((keyword.text, ad_group_criterion.criterion_id))
            # print(
            #     f'Keyword with text "{keyword.text}", match type '
            #     f"{keyword.match_type}, criteria type "
            #     f"{ad_group_criterion.type_}, and ID "
            #     f"{ad_group_criterion.criterion_id} was found in ad group "
            #     f"with ID {ad_group.id}."
            # )

        return {"status": 200, "data": keywords}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


# deletes a keyword
def delete_keyword(customer_id, ad_group_id, criterion_id):
    agc_service = client.get_service("AdGroupCriterionService")
    agc_operation = client.get_type("AdGroupCriterionOperation")

    resource_name = agc_service.ad_group_criterion_path(
        customer_id, ad_group_id, criterion_id
    )
    agc_operation.remove = resource_name

    try:
        agc_response = agc_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=[agc_operation]
        )

        keyword_id = agc_response.results[0].resource_name.split("/")[3].split("~")[1]

        return {"status": 200, "body": {"keyword_id":keyword_id}}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


# creates a responsive search ad
def create_new_responsive_search_ad(customer_id, ad_group_id, headlines_texts, descriptions_texts, final_url, pinned_text=None):
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_service = client.get_service("AdGroupService")

    # Create the ad group ad.
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.status = client.get_type(
        "AdGroupAdStatusEnum"
    ).AdGroupAdStatus.PAUSED
    ad_group_ad.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )

    # Set responsive search ad info.
    ad_group_ad.ad.final_urls.append(final_url)

    # Set a pinning to always choose this asset for HEADLINE_1. Pinning is
    # optional; if no pinning is set, then headlines and descriptions will be
    # rotated and the ones that perform best will be used more often.
    headlines = []
    if pinned_text:
        served_asset_enum = client.get_type(
            "ServedAssetFieldTypeEnum").ServedAssetFieldType.HEADLINE_1
        pinned_headline = _create_ad_text_asset(
            pinned_text, served_asset_enum)
        headlines.append(pinned_headline)


    for text in headlines_texts:
        headlines.append(_create_ad_text_asset(text))

    descriptions = []
    for text in descriptions_texts:
        descriptions.append(_create_ad_text_asset(text))

    ad_group_ad.ad.responsive_search_ad.headlines.extend(headlines)
    ad_group_ad.ad.responsive_search_ad.descriptions.extend(descriptions)
    ad_group_ad.ad.responsive_search_ad.path1 = "all-inclusive"
    ad_group_ad.ad.responsive_search_ad.path2 = "deals"

    # Send a request to the server to add a responsive search ad.
    try:
        ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=[ad_group_ad_operation]
        )

        ad_id = ad_group_ad_response.results[0].resource_name.split("/")[3].split("~")[1]
        return {"status": 200, "body": {"ad_id": ad_id}}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


def _create_ad_text_asset(text, pinned_field=None):
    """Create an AdTextAsset."""
    ad_text_asset = client.get_type("AdTextAsset")
    ad_text_asset.text = text
    if pinned_field:
        ad_text_asset.pinned_field = pinned_field
    return ad_text_asset


# returns responsive search ad by ad id
def get_responsive_search_ad_by_id(customer_id, ad_id):
    ga_service = client.get_service("GoogleAdsService")

    query = f'''
                SELECT ad_group.id, ad_group_ad.ad.id,
                ad_group_ad.ad.responsive_search_ad.headlines,
                ad_group_ad.ad.responsive_search_ad.descriptions,
                ad_group_ad.status FROM ad_group_ad
                WHERE ad_group_ad.ad.type = RESPONSIVE_SEARCH_AD and ad_group_ad.ad.id ={ad_id} 
                AND ad_group_ad.status != "REMOVED"'''

    ga_search_request = client.get_type("SearchGoogleAdsRequest")
    ga_search_request.customer_id = customer_id
    ga_search_request.query = query
    ga_search_request.page_size = _DEFAULT_PAGE_SIZE

    try:
        results = ga_service.search(request=ga_search_request)

        one_found = False

        ads = []
        for row in results:
            one_found = True
            ad = row.ad_group_ad.ad
            headlines = "\n".join(
                _ad_text_assets_to_strs(ad.responsive_search_ad.headlines))
            descriptions = "\n".join(
                _ad_text_assets_to_strs(ad.responsive_search_ad.descriptions))
            ads.append((ad.id, row.ad_group_ad.status.name, headlines, descriptions))

        if not one_found:
            return {"data": "No responsive search ads were found."}
        return {"status": 200, "data": ads}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)

# returns all responsive search ads belongs to ad_group_id
def get_all_responsive_search_ads(customer_id, ad_group_id):
    ga_service = client.get_service("GoogleAdsService")

    query = '''
            SELECT ad_group.id, ad_group_ad.ad.id,
            ad_group_ad.ad.responsive_search_ad.headlines,
            ad_group_ad.ad.responsive_search_ad.descriptions,
            ad_group_ad.status FROM ad_group_ad
            WHERE ad_group_ad.ad.type = RESPONSIVE_SEARCH_AD
            AND ad_group_ad.status != "REMOVED"'''

    # Optional: Specify an ad group ID to restrict search to only a given
    # ad group.
    if ad_group_id:
        query += f" AND ad_group.id = {ad_group_id}"

    ga_search_request = client.get_type("SearchGoogleAdsRequest")
    ga_search_request.customer_id = customer_id
    ga_search_request.query = query
    ga_search_request.page_size = _DEFAULT_PAGE_SIZE

    try:
        results = ga_service.search(request=ga_search_request)

        one_found = False

        ads = []
        for row in results:
            one_found = True
            ad = row.ad_group_ad.ad
            # print(
            #     "Responsive search ad with resource name "
            #     f'"{ad.resource_name}", status {row.ad_group_ad.status.name} '
            #     "was found.")
            headlines = "\n".join(
                _ad_text_assets_to_strs(ad.responsive_search_ad.headlines))
            descriptions = "\n".join(
                _ad_text_assets_to_strs(ad.responsive_search_ad.descriptions))
            ads.append((ad.id, row.ad_group_ad.status.name, headlines, descriptions))
            # print(f"Headlines:\n{headlines}\nDescriptions:\n{descriptions}\n")

        if not one_found:
            return {"data": "No responsive search ads were found."}
            # print("No responsive search ads were found.")
        return {"status": 200, "body": {"data": ads}}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


# deletes a keyword
def delete_ad(customer_id, ad_group_id, ad_id):
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")

    resource_name = ad_group_ad_service.ad_group_ad_path(
        customer_id, ad_group_id, ad_id
    )
    ad_group_ad_operation.remove = resource_name

    try:
        ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=[ad_group_ad_operation]
        )

        ad_id = ad_group_ad_response.results[0].resource_name.split("/")[3].split("~")[1]
        return {"status": 200, "data": "ad with id: " + ad_id + " deleted"}

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


def _ad_text_assets_to_strs(assets):
    """Converts a list of AdTextAssets to a list of user-friendly strings."""
    s = []
    for asset in assets:
        s.append(f"\t {asset.text} pinned to {asset.pinned_field.name}")
    return s


def get_statistics_to_csv(customer_id, output_file, write_headers, period):
    """Writes rows returned from a search_stream request to a CSV file.
        Args:
            customer_id (str): The client customer ID string.
            output_file (str): Filename of the file to write the report data to.
            write_headers (bool): True if arg is not provided.
            period (bool): False if arg is not provided. If True - the statistics of the campaigns from the last 30 days in given
        """
    ga_service = client.get_service("GoogleAdsService")
    output = []

    if period:
        query = """
                SELECT
                  customer.descriptive_name,
                  segments.date,
                  campaign.name,
                  metrics.impressions,
                  metrics.clicks,
                  metrics.cost_micros
                FROM campaign
                WHERE
                  segments.date DURING LAST_30_DAYS
                ORDER BY metrics.impressions DESC
                LIMIT 25"""
    else:
        query = """
                SELECT
                  customer.descriptive_name,
                  campaign.name,
                  metrics.impressions,
                  metrics.clicks,
                  metrics.cost_micros
                FROM campaign
                ORDER BY metrics.impressions DESC
                LIMIT 25"""


    # Issues a search request using streaming.
    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    response = ga_service.search_stream(search_request)
    try:
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)

            # Define a list of headers for the first row.
            headers = [
                "Account",
                "Date",
                "Campaign",
                "Impressions",
                "Clicks",
                "Cost",
            ]

            # If the write_headers flag was passed, write header row to the CSV
            if write_headers or write_headers is None:
                writer.writerow(headers)

            for batch in response:
                for row in batch.results:
                    # Use the CSV writer to write the individual GoogleAdsRow
                    # fields returned in the SearchGoogleAdsStreamResponse.
                    writer.writerow(
                        [
                            row.customer.descriptive_name,
                            row.segments.date,
                            row.campaign.name,
                            row.metrics.impressions,
                            row.metrics.clicks,
                            row.metrics.cost_micros,
                        ]
                    )
                    output.append(f'descriptive name "{row.customer.descriptive_name}" with '
                                  f'date "{row.segments.date}" and '
                                  f"campaign name {row.campaign.name}: "
                                  f'impressions "{row.metrics.impressions}", '
                                  f'clicks "{row.metrics.clicks}", '
                                  f'cost (micros) "{row.metrics.cost_micros}"')

        return {"status": 200, "body":{"stats":output} }

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


def get_keyword_stats(customer_id, output_file, write_headers):
    # the statistics are from the last 7 days
    ga_service = client.get_service("GoogleAdsService")
    output = []

    query = """
            SELECT
              campaign.id,
              campaign.name,
              ad_group.id,
              ad_group.name,
              ad_group_criterion.criterion_id,
              ad_group_criterion.keyword.text,
              ad_group_criterion.keyword.match_type,
              metrics.impressions,
              metrics.clicks,
              metrics.cost_micros
            FROM keyword_view WHERE segments.date DURING LAST_30_DAYS
            AND campaign.advertising_channel_type = 'SEARCH'
            AND ad_group.status = 'ENABLED'
            AND ad_group_criterion.status IN ('ENABLED', 'PAUSED')
            ORDER BY metrics.impressions DESC
            LIMIT 50"""

    # Issues a search request using streaming.
    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    response = ga_service.search_stream(search_request)
    try:
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)

            # Define a list of headers for the first row.
            headers = [
                "Keyword text",
                "match type",
                "Keyword ID",
                "ad group name",
                "ad group ID",
                "campaign name",
                "campaign ID",
                "impression(s)",
                "click(s)",
                "cost (in micros)",
            ]

            # If the write_headers flag was passed, write header row to the CSV
            if write_headers or write_headers is None:
                writer.writerow(headers)


            for batch in response:
                for row in batch.results:
                    # Use the CSV writer to write the individual GoogleAdsRow
                    # fields returned in the SearchGoogleAdsStreamResponse.
                    campaign = row.campaign
                    ad_group = row.ad_group
                    criterion = row.ad_group_criterion
                    metrics = row.metrics
                    writer.writerow(
                        [
                            criterion.keyword.text,
                            criterion.keyword.match_type.name,
                            criterion.criterion_id,
                            ad_group.name,
                            ad_group.id,
                            campaign.name,
                            campaign.id,
                            metrics.impressions,
                            metrics.clicks,
                            metrics.cost_micros,
                        ]
                    )
                    output.append(f'Keyword text "{criterion.keyword.text}" with '
                                  f'match type "{criterion.keyword.match_type.name}" '
                                  f"and ID {criterion.criterion_id} in "
                                  f'ad group "{ad_group.name}" '
                                  f'with ID "{ad_group.id}" '
                                  f'in campaign "{campaign.name}" '
                                  f"with ID {campaign.id} "
                                  f"had {metrics.impressions} impression(s), "
                                  f"{metrics.clicks} click(s), and "
                                  f"{metrics.cost_micros} cost (in micros) during "
                                  "the last 7 days.")

        return {"status": 200, "body":{"keywordStats":output} }

    except GoogleAdsException as ex:
        return _handle_googleads_exception(ex)


# [START add_campaign_targeting_criteria_1]
def _create_location_op(customer_id, campaign_id, locations):
    campaign_service = client.get_service("CampaignService")
    geo_target_constant_service = client.get_service("GeoTargetConstantService")

    gtc_request = client.get_type("SuggestGeoTargetConstantsRequest")

    gtc_request.locale = "en"
    gtc_request.country_code = "US"

    # The location names to get suggested geo target constants.
    gtc_request.location_names.names.extend(locations)

    results = geo_target_constant_service.suggest_geo_target_constants(gtc_request)

    location_id = 0

    # if not results.geo_target_constant_suggestions:
    #     return {"status": 400, "body": "There is no locations that match your request"}

    for suggestion in results.geo_target_constant_suggestions:
        geo_target_constant = suggestion.geo_target_constant
        location_id = geo_target_constant.id
        print(
            f"{geo_target_constant.resource_name} "
            f"{geo_target_constant.id} "
            f"({geo_target_constant.name}, "
            f"{geo_target_constant.country_code}, "
            f"{geo_target_constant.target_type}, "
            f"{geo_target_constant.status.name}) "
            f"is found in locale ({suggestion.locale}) "
            f"with reach ({suggestion.reach}) "
            f"from search term ({suggestion.search_term})."
        )

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type("CampaignCriterionOperation")
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    # Besides using location_id, you can also search by location names from
    # GeoTargetConstantService.suggest_geo_target_constants() and directly
    # apply GeoTargetConstant.resource_name here. An example can be found
    # in get_geo_target_constant_by_names.py.
    campaign_criterion.location.geo_target_constant = geo_target_constant_service.geo_target_constant_path(
        location_id
    )

    return campaign_criterion_operation
    #todo json?, add?
    #[END add_campaign_targeting_criteria_1]


# [START add_campaign_targeting_criteria_3]
def _create_age_op(customer_id, campaign_id, min_age, max_age):
    campaign_service = client.get_service("CampaignService")

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type("CampaignCriterionOperation")
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    campaign_criterion.negative = True
    # todo handle the problem
    if min_age == 25 and max_age == 34:
        campaign_criterion.age_range.type_ = client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_25_34

    # if age in Enum.Age_1.keys():
    #     Enum.Age_1[age]()
    # # todo check default, check if working
    # else:
    #      campaign_criterion.age_range.type_ = client.get_type("AgeRangeTypeEnum").AgeRangeType.AGE_RANGE_25_34
    #
    return campaign_criterion_operation
    # [END add_campaign_targeting_criteria_3]
     # todo json?, add?

# [START add_campaign_targeting_criteria_4]
def _create_gender_op(customer_id, campaign_id, gender):
    campaign_service = client.get_service("CampaignService")

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type("CampaignCriterionOperation")
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    campaign_criterion.negative = True
    if gender in Enum.Gender.keys():
        campaign_criterion.gender.type_ = Enum.Gender[gender]()
    else:
        campaign_criterion.gender.type_ = client.get_type("GenderTypeEnum").GenderType.UNDETERMINED

        # campaign_criterion.gender.type_ = client.get_type("GenderTypeEnum").GenderType.FEMALE
    return campaign_criterion_operation
    # [END add_campaign_targeting_criteria_4]
    # todo json?, add?

# [START add_campaign_targeting_criteria_5]
def _create_device_op(customer_id, campaign_id, device_type):
    campaign_service = client.get_service("CampaignService")

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type("CampaignCriterionOperation")
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )
    #todo check if work, defult
    if device_type in Enum.Gender.keys():
        campaign_criterion.device.type_= Enum.Gender[device_type]()
    else:
        campaign_criterion.device.type_ = client.get_type("DeviceEnum").Device.DESKTOP

    return campaign_criterion_operation
    # [END add_campaign_targeting_criteria_5]
    # todo json?, add?

# [START add_campaign_targeting_criteria_6]
def _create_operating_system_op(customer_id, campaign_id):
    campaign_service = client.get_service("CampaignService")

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type("CampaignCriterionOperation")
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    campaign_criterion.operating_system_version.operating_system_version_constant = "operatingSystemVersionConstants/Android4.2.2"
    return campaign_criterion_operation
    # [END add_campaign_targeting_criteria_6]
# todo json?, add?

# [START add_campaign_targeting_criteria_7]
def _create_user_interest_op(customer_id, campaign_id, interest):
    campaign_service = client.get_service("CampaignService")

    # Get the id of the interests
    # Get the GoogleAdsService client.
    googleads_service = client.get_service("GoogleAdsService")

    # Create a query that retrieves the targetable user interests constants by name.

    query = f"""
                SELECT user_interest.name, user_interest.user_interest_id, user_interest.resource_name
                FROM user_interest
                WHERE user_interest.name LIKE '%{interest}%'
                """

    # Issue a search request and process the stream response to print the
    # requested field values for the user interest constant in each row.
    response = googleads_service.search_stream(
        customer_id=customer_id, query=query
    )

    for batch in response:
        for row in batch.results:
            print(
                f"User interest with ID {row.user_interest.user_interest_id}, "
                f"category '{row.user_interest.name}'"
                f"resource name '{row.user_interest.resource_name}' "
            )
            resource_name = row.user_interest.resource_name

    # Create the campaign criterion.
    campaign_criterion_operation = client.get_type("CampaignCriterionOperation")
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    campaign_criterion.user_interest.user_interest_category = resource_name

    return campaign_criterion_operation
    # [END add_campaign_targeting_criteria_7]
# todo json?, add?

# todo fix the \n in the message
# todo status code 400??
def _handle_googleads_exception(exception):
    res = f'Request with ID "{exception.request_id}" failed with status "{exception.error.code().name}" and includes the following errors:\n'
    # print(
    #     f'Request with ID "{exception.request_id}" failed with status '
    #     f'"{exception.error.code().name}" and includes the following errors:'
    # )
    temp = ""
    for error in exception.failure.errors:
        temp = temp + f'\tError with message "{error.message}".\n'
        # print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                temp = temp + f"\t\tOn field: {field_path_element.field_name}\n"
                # print(f"\t\tOn field: {field_path_element.field_name}")
    return {"status": 400, "body": res+temp}