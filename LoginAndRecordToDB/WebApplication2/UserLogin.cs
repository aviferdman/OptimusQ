using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace WebApplication2
{
    public class UserLogin
    {
        public DateTime Date { get; set; }
        public string UserID { get; set; }

        public UserLogin(string userId)
        {
            Date = DateTime.Now;
            UserID = userId;
        }
    }
}
