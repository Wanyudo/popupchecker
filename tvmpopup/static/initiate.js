var form = document.getElementById('form-params');
var loader = document.getElementById('loader');

document.getElementById('submitter').addEventListener("click", function(e){
  form.style.display = 'none';
  loader.style.display = 'flex';
  e.preventDefault();

  const res = document.getElementById('res').value;
  const domain = document.getElementById('domain').value;
  const code = document.getElementById('code').value;
  const lang = document.getElementById('lang').value;

  axios.get('/popups/?res='+ res + "&domain=" + domain + "&code=" + code + "&language=" + lang)
  .then(function (response) {
    var list = response.data;
    var dom_list = document.getElementById('screens-list');
    for(screen in list){
      var link = document.createElement('a');
      link.classList.add('link');
      link.href = list[screen];
      link.target = "_blank";
      var name = document.createElement('div');
      name.innerHTML = screen;
      name.classList.add('popup-name');
      link.appendChild(name);
      var image = document.createElement('img');
      image.src = link.href;
      image.classList.add('popup-image');
      link.appendChild(image);
      dom_list.appendChild(link);
    }
    loader.style.display = 'none';
    dom_list.style.display = 'flex';
  })
  .catch(function (error) {
    loader.style.display = 'none';
    document.getElementById('error').display = 'flex';
    console.log(error);
  })
});
