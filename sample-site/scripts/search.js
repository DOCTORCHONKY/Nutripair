// Update this variable to point to your domain.
var apigatewayendpoint = 'https://xqfggpp8hi.execute-api.us-west-1.amazonaws.com/opensearch-api-test/opensearch-lambda';
var loadingdiv = $('#loading');
var noresults = $('#noresults');
var resultdiv = $('#results');
var searchbox = $('input#search');
var timer = 0;

// Executes the search function 250 milliseconds after user stops typing
searchbox.keyup(function () {
  clearTimeout(timer);
  timer = setTimeout(search, 250);
});

async function search() {
  // Clear results before searching
  noresults.hide();
  resultdiv.empty();
  loadingdiv.show();
  // Get the query from the user
  let query = searchbox.val();
  // Only run a query if the string contains at least three characters
  if (query.length > 2) {
    // Make the HTTP request with the query as a parameter and wait for the JSON results
    let response = await $.get(apigatewayendpoint, { q: query, size: 30 }, 'json');
    // Get the part of the JSON response that we care about
    let results = response['hits']['hits'];
	  console.log(results);
    if (results.length > 0) {
      loadingdiv.hide();
      // Iterate through the results and write them to HTML
      resultdiv.append('<p>Found ' + results.length + ' results</p>');
      resultdiv.append('<p class="note">*Amount per 100 g</p>');

      for (var item in results) {
        let des = results[item]._source.Food_Description;
        let cal = results[item]._source.Energy_kcal;
        let protein = results[item]._source.Protein_g;
        let fat = results[item]._source.Total_Fat_g;
        let carb = results[item]._source.Carbohydrate_g;
        // Construct the full HTML string that we want to append to the div
        resultdiv.append('<div class="result"> <h2>' + des +' </h2> <div> <p>Calories ' + cal +' </p > <p>Protein ' + protein + ' </p> <p>Total Fat ' + fat + ' </p><p>Carbohydrate ' + carb + ' </p></div ></div>');
      }
    } else {
      noresults.show();
    }
  }
  loadingdiv.hide();
}

// Tiny function to catch images that fail to load and replace them
function imageError(image) {
  image.src = 'images/no-image.png';
}
