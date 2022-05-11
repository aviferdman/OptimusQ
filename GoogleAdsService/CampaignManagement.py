import datetime
import sys
import uuid
import os

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

_DATE_FORMAT = "%Y%m%d"
_DEFAULT_PAGE_SIZE = 1000

# This interface allows the user to create and manage all the marketing fields,
# using Google Ads APIs.
dir_path = os.path.dirname(os.path.realpath(__file__))
curr_path = dir_path + "\google-ads.yaml"
client = GoogleAdsClient.load_from_storage(path=curr_path, version="v9")


# creates a new campaign
def create_new_campaign(customer_id, budget, name, days_to_start, weeks_to_end, status):
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_service = client.get_service("CampaignService")

    # [START add_campaigns]
    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Interplanetary Budget {uuid.uuid4()}"
    campaign_budget.delivery_method = client.get_type(
        "BudgetDeliveryMethodEnum"
    ).BudgetDeliveryMethod.STANDARD
    campaign_budget.amount_micros = 1000000 * budget

    # Add budget.
    try:
        campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[campaign_budget_operation]
        )
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)
        # [END add_campaigns]

    # [START add_campaigns_1]
    # Create campaign.
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = name
    campaign.advertising_channel_type = client.get_type(
        "AdvertisingChannelTypeEnum"
    ).AdvertisingChannelType.SEARCH

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
    # [END add_campaigns_1]

    # Optional: Set the start date.
    start_time = datetime.date.today() + datetime.timedelta(days=days_to_start)
    campaign.start_date = datetime.date.strftime(start_time, _DATE_FORMAT)

    # Optional: Set the end date.
    end_time = start_time + datetime.timedelta(weeks=weeks_to_end)
    campaign.end_date = datetime.date.strftime(end_time, _DATE_FORMAT)

    # Add the campaign.
    try:
        campaign_response = campaign_service.mutate_campaigns(
            customer_id="5103537456", operations=[campaign_operation]
        )
        return {"body": campaign_response.results[0].resource_name}
        # print(f"Created campaign {campaign_response.results[0].resource_name}.")
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)

# returns all campaign belongs to AD_ACCOUNT_ID
def get_all_campaigns(customer_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
            SELECT
              campaign.id,
              campaign.name
            FROM campaign
            ORDER BY campaign.id"""

    # Issues a search request using streaming.
    response = ga_service.search_stream(customer_id=customer_id, query=query)

    campaigns = []
    for batch in response:
        for row in batch.results:
            campaigns.append((row.campaign.id,row.campaign.name))
            # print(f"Campaign with ID {row.campaign.id} and name "
            #       f'"{row.campaign.name}" was found.')
    return {"body": campaigns}

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
    response = ga_service.search_stream(customer_id=customer_id, query=query)

    campaigns = []
    for batch in response:
        for row in batch.results:
            campaigns.append((row.campaign.id, row.campaign.name))
    return {"body": campaigns}

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
    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation])
    return {"body": ad_group_response.results[0].resource_name}
    # print(f"Created ad group {ad_group_response.results[0].resource_name}.")

# returns all ad groups belongs to campaign_id
def get_all_ad_groups(customer_id, campaign_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
            SELECT
              campaign.id,
              ad_group.id,
              ad_group.name
            FROM ad_group"""

    if campaign_id:
        query += f" WHERE campaign.id = {campaign_id}"

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = _DEFAULT_PAGE_SIZE

    results = ga_service.search(request=search_request)

    ad_groups = []
    for row in results:
        ad_groups.append((row.ad_group.id, row.ad_group.name))
        # print(
        #     f"Ad group with ID {row.ad_group.id} and name "
        #     f'"{row.ad_group.name}" was found in campaign with '
        #     f"ID {row.campaign.id}.")
    return {"body": ad_groups}

# adds a keyword to an ad group
def add_keyword(customer_id, ad_group_id, keyword_text):
    ad_group_service = client.get_service("AdGroupService")
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    # Create keyword.
    ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group_criterion.status = client.get_type(
        "AdGroupCriterionStatusEnum"
    ).AdGroupCriterionStatus.ENABLED
    ad_group_criterion.keyword.text = keyword_text
    ad_group_criterion.keyword.match_type = client.get_type(
        "KeywordMatchTypeEnum"
    ).KeywordMatchType.EXACT

    # Optional field
    # All fields can be referenced from the protos directly.
    # The protos are located in subdirectories under:
    # https://github.com/googleapis/googleapis/tree/master/google/ads/googleads
    # ad_group_criterion.negative = True

    # Optional repeated field
    # ad_group_criterion.final_urls.append('https://www.example.com')

    # Add keyword
    ad_group_criterion_response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=[ad_group_criterion_operation],
    )

    # print(
    #     "Created keyword "
    #     f"{ad_group_criterion_response.results[0].resource_name}."
    # )
    return {"body": ad_group_criterion_response.results[0].resource_name}

# gets the keywords of an ad group
def get_keywords(customer_id, ad_group_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
            SELECT
              ad_group.id,
              ad_group_criterion.type,
              ad_group_criterion.criterion_id,
              ad_group_criterion.keyword.text,
              ad_group_criterion.keyword.match_type
            FROM ad_group_criterion
            WHERE ad_group_criterion.type = KEYWORD"""

    if ad_group_id:
        query += f" AND ad_group.id = {ad_group_id}"

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = _DEFAULT_PAGE_SIZE

    results = ga_service.search(request=search_request)

    keywords = []
    for row in results:
        ad_group = row.ad_group
        ad_group_criterion = row.ad_group_criterion
        keyword = row.ad_group_criterion.keyword

        keywords.append(keyword.text)
        # print(
        #     f'Keyword with text "{keyword.text}", match type '
        #     f"{keyword.match_type}, criteria type "
        #     f"{ad_group_criterion.type_}, and ID "
        #     f"{ad_group_criterion.criterion_id} was found in ad group "
        #     f"with ID {ad_group.id}."
        # )

    return {"data": keywords}

# todo throw exception if the headings is less than 3and descriptions is less than 2
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
            "ServedAssetFieldTypeEnum"
        ).ServedAssetFieldType.HEADLINE_1
        pinned_headline = _create_ad_text_asset(
            pinned_text, served_asset_enum
        )
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
    ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )

    res = []
    for result in ad_group_ad_response.results:
        res.append(result.resource_name)
        # print(
        #     f"Created responsive search ad with resource name "
        #     f'"{result.resource_name}".'
        # )
    return {"body": res}

def _create_ad_text_asset(text, pinned_field=None):
    """Create an AdTextAsset."""
    ad_text_asset = client.get_type("AdTextAsset")
    ad_text_asset.text = text
    if pinned_field:
        ad_text_asset.pinned_field = pinned_field
    return ad_text_asset

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
    return {"data": ads}


def _ad_text_assets_to_strs(assets):
    """Converts a list of AdTextAssets to a list of user-friendly strings."""
    s = []
    for asset in assets:
        s.append(f"\t {asset.text} pinned to {asset.pinned_field.name}")
    return s




def _handle_googleads_exception(exception):
    print(
        f'Request with ID "{exception.request_id}" failed with status '
        f'"{exception.error.code().name}" and includes the following errors:'
    )
    for error in exception.failure.errors:
        print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"\t\tOn field: {field_path_element.field_name}")
    sys.exit(1)