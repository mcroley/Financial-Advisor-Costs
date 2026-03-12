using Microsoft.AspNetCore.Mvc;
using FinancialAdvisorCosts.Models;

namespace FinancialAdvisorCosts.Controllers
{
    public class InvestmentsController : Controller
    {
        [HttpGet]
        public IActionResult Index()
        {
            var model = new InvestmentModel();
            return View(model);
        }

        [HttpPost]
        public IActionResult Index(InvestmentModel model)
        {
            if (!ModelState.IsValid)
            {
                return View(model);
            }

            // Mark as calculated to display results
            model.IsCalculated = true;
            return View(model);
        }
    }
}
