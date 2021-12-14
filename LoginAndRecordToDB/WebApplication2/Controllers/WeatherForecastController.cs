using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using MongoDB.Driver;
using Microsoft.Data.SqlClient;
using System.Text;



namespace WebApplication2.Controllers
{
    

    [ApiController]
    [Route("[controller]")]
    public class WeatherForecastController : ControllerBase
    {
        
        public static MongoClientSettings settings = MongoClientSettings.FromConnectionString("mongodb+srv://dorc:iloveJ20@optimusdbdemo.xoeys.mongodb.net/myFirstDatabase?retryWrites=true&w=majority");
        public static MongoClient client = new MongoClient(settings);
        public string databaseName = "OptimusDbDemo";
        public string collectionName = "weather";


        private List<WeatherForecast> weathers;
        private static readonly string[] Summaries = new[]
        {
            "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
        };

        private readonly ILogger<WeatherForecastController> _logger;

        public WeatherForecastController(ILogger<WeatherForecastController> logger)
        {
            _logger = logger;
            weathers = new List<WeatherForecast>();
            SqlConnectionStringBuilder builder = new SqlConnectionStringBuilder();
            builder.DataSource = "optimusbgudb.database.windows.net";

            

            


        }

        [HttpGet]
        public IEnumerable<WeatherForecast> Get()
        {
            var rng = new Random();
            return Enumerable.Range(1, 5).Select(index => new WeatherForecast
            {
                Date = DateTime.Now.AddDays(index),
                TemperatureC = rng.Next(-20, 55),
                Summary = Summaries[rng.Next(Summaries.Length)]
            })
            .ToArray();
        }

        [HttpPost]
        public async void Set()
        {
            var db = WeatherForecastController.client.GetDatabase(databaseName);
            var collection = db.GetCollection<WeatherForecast>(collectionName);
            WeatherForecast weatherForecast = new WeatherForecast();
            weatherForecast.Date = DateTime.Now;
            weatherForecast.Summary = "shfgdijglk";
            weatherForecast.TemperatureC = 50;

            await collection.InsertOneAsync(weatherForecast);
            string connectionString = "Server=tcp:optimusbgudb.database.windows.net,1433;Initial Catalog=Optimus-BGU-db;Persist Security Info=False;User ID=Optimus-BGU-db;Password=avidorgilTheBest2022;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;";
            using (var con = new SqlConnection(connectionString))
            {
                using (var command = con.CreateCommand())
                {
                    command.CommandText = @"
                        CREATE TABLE connections (
                            Date    DATETIME,
                            UserID  VARCHAR(30)
                        );
    
                    ";
                    con.Open();
                    command.ExecuteNonQuery();
                }
            }

            weathers.Add(new WeatherForecast());
        }
    }
}
