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






const tabsButtons = document.querySelectorAll('.tab');

// Проходимся по всем кнопкам
tabsButtons.forEach(btn => {
  // вешаем на каждую кнопку обработчик события клик
  btn.addEventListener('click', () => {
    // Удаляем класс _active у всех кнопок
    tabsButtons.forEach(button => button.classList.remove('_active'));

    // Получаем предыдущую активную вкладку
    const prevActiveItem = document.querySelector('.allm._active');
    
    // Удаляем класс _active у предыдущей вкладки если она есть
    if (prevActiveItem) {
      prevActiveItem.classList.remove('_active');
    }

    // получаем id новой активной вкладки, который мы перем из атрибута data-tab у кнопки
    const nextActiveItemId = `#${btn.getAttribute('data-tab')}`;
    // получаем новую активную вкладку по id
    const nextActiveItem = document.querySelector(nextActiveItemId);
    
    // добавляем класс _active кнопке на которую нажали
    btn.classList.add('_active');
    // добавляем класс _active новой выбранной вкладке
    nextActiveItem.classList.add('_active');
  });
});
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
  
  function changeText () {
    let text = document.getElementById('text');
    text.innerHTML = `<textarea>${text.textContent}</textarea>`
  }
  // Получаем input элементы
  var discordNick = document.getElementById('discordNick');
  var nickname = document.getElementById('nickname');
  var email = document.getElementById('email');
  var birthdate = document.getElementById('birthdate');
  var editButton = document.getElementById('editButton');
  var saveButton = document.getElementById('saveButton');
  
  // Загружаем сохраненные данные при загрузке страницы
  window.onload = function() {
    if(localStorage.getItem('discordNick')) {
      discordNick.value = localStorage.getItem('discordNick');
    }
    if(localStorage.getItem('nickname')) {
      nickname.value = localStorage.getItem('nickname');
    }
    if(localStorage.getItem('email')) {
      email.value = localStorage.getItem('email');
    }
    if(localStorage.getItem('birthdate')) {
      birthdate.value = localStorage.getItem('birthdate');
    }
  };
  
  // Функция для переключения режима редактирования

  // Get the button
// Get the button
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