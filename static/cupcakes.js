const BASE_URL = 'http://localhost:5000';

function generateCupcakeHTML(cupcake) {
  return `
    <div class="col-sm-2">
    <button class="delete-cupcake btn-sm btn-danger" data-id="${cupcake.id}">X</button>
    <img class="img-thumbnail" src="${cupcake.image}" alt=" RIP cupcake image was supposed to go here">
    <p class="text-primary font-italic"><b>Flavor: </b> ${cupcake.flavor}</p>
        <p class="text-info font-italic "><b>Size: </b> ${cupcake.size}</p>
    <p class="text-success font-italic "> <b>Rating: </b> ${cupcake.rating}</p>
</div>
`;
}


async function showCupcakes() {
  const response = await axios.get(`${BASE_URL}/api/cupcakes`);

  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(generateCupcakeHTML(cupcakeData));
    $('#cupcakes-list').append(newCupcake);
  }
}


$('#new-cupcake-form').on('submit', async function (evt) {
  evt.preventDefault();

  let flavor = $('#form-flavor').val();
  let size = $('#form-size').val();
  let rating = $('#form-rating').val();
  let image = $('#form-image').val();

  const response = await axios.post(`${BASE_URL}/api/cupcakes`, {
    flavor,
    size,
    rating,
    image
  });

  let newCupcake = $(generateCupcakeHTML(response.data.cupcake));
  $('#cupcakes-list').append(newCupcake);
  $('#new-cupcake-form').trigger('reset');
});


$(document).ready(function () {
  // showCupcakes();
});


$('.delete-cupcake').click(deleteCupcake)

async function deleteCupcake() {
  const id = $(this).data('id')
  await axios.delete(`${BASE_URL}/api/cupcakes/${id}`)
  $(this).parent().remove()
}