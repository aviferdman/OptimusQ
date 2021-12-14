using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using MongoDB.Bson.Serialization.Attributes;
using MongoDB.Bson;

namespace WebApplication2
{
    public class WeatherForecast
    {
        [BsonId]
        [BsonRepresentation(BsonType.DateTime)]
        public DateTime Date { get; set; }

        public int TemperatureC { get; set; }

        public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);

        public string Summary { get; set; }
    }

    [ApiController]
    [Route("[controller]")]
    public class WeatherController
    {
        public static WeatherController weatherController= new WeatherController();

        public List<WeatherForecast> weathers;
        public WeatherController()
        {
            this.weathers = new List<WeatherForecast>();
        }

        [HttpPost]
        public void Insert()
        {
            this.weathers.Add(new WeatherForecast());
        }
    }
}
