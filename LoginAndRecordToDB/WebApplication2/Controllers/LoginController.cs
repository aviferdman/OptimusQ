using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.SqlClient;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WebApplication2.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class LoginController : ControllerBase
    {
        private string connectionString="Server=tcp:optimusbgudb.database.windows.net,1433;Initial Catalog=Optimus-BGU-db;Persist Security Info=False;User ID=Optimus-BGU-db;Password=avidorgilTheBest2022;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;";
        public LoginController()
        {
            
        }

        [HttpPost()]
        public void Login([FromQuery]string id)
        {

            UserLogin userLogin = new UserLogin(id);
            using (var con = new SqlConnection(connectionString))
            {
                using (var command = con.CreateCommand())
                {
                    string que = String.Format(@"
                        INSERT INTO connections (Date,UserID)
                        VALUES('{0}','{1}');
                    ", userLogin.Date.ToString("yyyyMMdd hh:mm:ss"), userLogin.UserID);
                    command.CommandText = que;
                    con.Open();
                    try
                    {
                        command.ExecuteNonQuery();
                    }
                    catch(Exception ex)
                    {
                        Console.WriteLine(ex.Message);
                    }
                }
            }

        }
    }
}
