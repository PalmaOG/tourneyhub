var modal = document.getElementById('myMoodal');


var btn = document.getElementById("myBtn");


var span = document.getElementsByClassName("cloose")[0];

var modal1 = document.getElementById('myMoodal1');

var btn1 = document.getElementById("myBtn1");

var btn2 = document.getElementById("myBtn2");

var span1 = document.getElementsByClassName("cloose1")[0];


btn.onclick = function() {     // Нажатие на иконку профиля
    modal.style.display = "block";          
}


span.onclick = function() {    // Нажатие на крестик(Вход)
    modal.style.display = "none";
}


window.onclick = function(event) {     // Нажатие за границами модалки (Вход)
    if (event.target == modal) {
        modal.style.display = "none";
    }
}


btn1.onclick = function() {    // Нажатие на кнопку "Регистрация"
    modal.style.display = "none";
    modal1.style.display = "block";
}

btn2.onclick = function() {    // Нажатие на кнопку "Вход"
    modal1.style.display = "none";
    modal.style.display = "block";
}

span1.onclick = function() {   // Нажатие на крестик(Регистрация)
    modal1.style.display = "none";
}


window.onclick = function(event) {    // Нажатие за границами модалки (Регистрация)
    if (event.target == modal1) {
        modal1.style.display = "none";
    }
}
document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.news-container .anynews');
    const itemsToShow = 5;
    let currentItems = 0;
  
    // Функция для отображения элементов
    function showItems() {
      for (let i = currentItems; i < currentItems + itemsToShow; i++) {
        if (items[i]) {
          items[i].style.display = 'block';
        }
      }
      currentItems += itemsToShow;
  
      // Если все элементы отображены, скрыть кнопку
      if (currentItems >= items.length) {
        document.getElementById('showMore').style.display = 'none';
      }
    }
  
    // Первоначально показываем первые пять элементов
    showItems();
  
    // Добавляем обработчик событий на кнопку "Show More"
    document.getElementById('showMore').addEventListener('click', showItems);
  });
  
  function searchTextOnPage() {
    var query = document.getElementById('searchInput').value;
    if (!query) {
      return false;
    }
    
    if (window.find) {
      // Для браузеров, поддерживающих window.find
      if (window.find(query)) {
        document.execCommand('hiliteColor', false, 'yellow');
      }
    } else {
      // Для браузеров, не поддерживающих window.find
      let text = document.getElementById('contentt').textContent || document.getElementById('contentt').innerText;
      let matchPosition = text.indexOf(query);
      
      if (matchPosition >= 0) {
        // Если текст найден, можно выделить его
        let range = document.createRange();
        let sel = window.getSelection();
        range.setStart(text, matchPosition);
        range.setEnd(text, matchPosition + query.length);
        sel.removeAllRanges();
        sel.addRange(range);
        document.execCommand('hiliteColor', false, 'yellow');
        return true;
      } else {
        console.log('Текст не найден.');
        return false;
      }
    }
  }


var maxSize = 1048576; // Максимальный размер файла - 1 мб
// script.js
document.addEventListener('DOMContentLoaded', function() {
  // Get the button
  let mybutton = document.getElementById("scrollToTopBtn");
  let scrollTimeout;

  // When the user scrolls down 20px from the top of the document, show the button
  window.onscroll = function() {
      scrollFunction();
  };

  function scrollFunction() {
      if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
          mybutton.style.display = "block";
          resetScrollTimeout();
      } else {
          mybutton.style.display = "none";
      }
  }

  function resetScrollTimeout() {
      if (scrollTimeout) {
          clearTimeout(scrollTimeout);
      }
      scrollTimeout = setTimeout(function() {
          mybutton.style.display = "none";
      }, 1500); // Hide the button after 2 seconds of no scrolling
  }

  // When the user clicks on the button, scroll to the top of the document
  mybutton.onclick = function() {
      document.body.scrollTop = 0; // For Safari
      document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
  };
});
const fileInput = document.getElementById('ShowExp');
fileInput.addEventListener('change', (e) => {
  const fileInfo = e.target.files[0];
  console.log(`Размер: ${fileInfo.size} `)
  if(fileInfo.size > maxSize) {
    alert('Размер файла не должен превышать 1 МБ! Пожалуйста, выберите другой файл.');
  }
  else
  {
    
    const reader = new FileReader();
    reader.onload = (e) => {
    document.getElementById('profilePhoto').src = e.target.result;
    };
    reader.readAsDataURL(fileInfo);
    console.log(`Файл: ${fileInfo.name}`);
  }
  
});
// Клик чтобы изменить фотку профиля
var link = document.getElementById('addphoto');
link.onclick = function() {
  document.getElementById('ShowExp').click(); 
}


var redact = document.getElementById('editButton');
redact.onclick = function() {
  document.getElementById('formprof').style.display='block';
  document.getElementById('addphoto').style.display='block';
  document.getElementById('nick_name').style.display='none';
  document.getElementById('nick_name1').style.display='none';
  document.getElementById('ShowExp').disabled = false;
  document.getElementById('Fname').disabled = false;
  document.getElementById('Lname').disabled = false;
  document.getElementById('Birth').disabled = false;
  document.getElementById('Discord').disabled = false;
  document.getElementById('Nickname').disabled = false;
  document.getElementById('Email').disabled = false;
  document.getElementById('submitButton').style.display="block";
  document.getElementById('undoButton').style.display="block";
  redact.style.display="none";
}

var und = document.getElementById('undoButton');
und.onclick = function() {
  document.getElementById('formprof').style.display='none';
  document.getElementById('addphoto').style.display='none';
  document.getElementById('nick_name').style.display='block';
  document.getElementById('nick_name1').style.display='block';
  document.getElementById('ShowExp').disabled = true;
  document.getElementById('Fname').disabled = true;
  document.getElementById('Lname').disabled = true;
  document.getElementById('Birth').disabled = true;
  document.getElementById('Discord').disabled = true;
  document.getElementById('Nickname').disabled = true;
  document.getElementById('Email').disabled = true;
  document.getElementById('submitButton').style.display="none";
  document.getElementById('editButton').style.display="block";
  und.style.display="none";
}
