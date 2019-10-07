document.getElementById('submitter').addEventListener("click", function(e){
  e.preventDefault();
  var form = document.getElementById('form-params');
  var progressElement = document.getElementById('progress');
  var loader_wrapper = document.getElementById('loader-wrapper');
  var codefield = document.getElementById('code');

  function isValidCode(code){
    if (code === '*enter your code*')
      return false;
    else return code.length >= 6;
  }

  if (!isValidCode(codefield.value)){
    document.getElementById('form-error').style.display = "block";
    return;
  }

  form.style.display = 'none';
  loader_wrapper.style.display = 'flex';
  const res = document.getElementById('res').value;
  const domain = document.getElementById('domain').value;
  const code = document.getElementById('code').value;
  const lang = document.getElementById('lang').value;
  const segment = document.getElementById('segment').value.toLowerCase();

  var progress = 0;
  var fullprogress = 100;
  var list = {};

  callAPI();

  function callAPI() {
    axios.get('/popups/?res=' + res + "&domain=" + domain + "&code=" + code + "&language=" + lang + "&progress=" + progress + "&segment=" + segment)
        .then(function (response) {
          for (item in response.data){
            if (response.data.hasOwnProperty(item))
              list[item] = response.data[item];
          }
        })
        .catch(function (error) {
          fullprogress -= 10;
          loader_wrapper.style.display = 'none';
          document.getElementById('error').style.display = 'flex';
          console.log(error);
        }).finally(function () {
      if (progress !== fullprogress) {
        callAPI();
        progress += 10;
        progressElement.innerText = progress + '%';
      } else {
        final();
      }
    });
  }

  function final() {
    var dom_list = document.getElementById('screens-list');
    for (screen in list) {
      var link = document.createElement('a');
      link.classList.add('link');
      if (list.hasOwnProperty(screen))
        link.href = list[screen];
      else
        link.href = '';
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
    loader_wrapper.style.display = 'none';
    dom_list.style.display = 'flex';
  }
});
