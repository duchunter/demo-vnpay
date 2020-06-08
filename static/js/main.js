$(document).ready(function() {
  const HOST = 'http://localhost:8000'
  // const HOST = 'https://itss-server.herokuapp.com'

  const BOT_ID = 'East Laos'

  var socket = io.connect(HOST);


  socket.on('connect', function() {
      console.log('Connected');
  });

  $('#forward').on('click', function() {
      socket.emit('manual', { id: BOT_ID, action: 'forward' });
  });

  $('#backward').on('click', function() {
      socket.emit('manual', { id: BOT_ID, action: 'backward' });
  });

  $('#right').on('click', function() {
      socket.emit('manual', { id: BOT_ID, action: 'right' });
  });

  $('#left').on('click', function() {
      socket.emit('manual', { id: BOT_ID, action: 'left' });
  });

  $('#up').on('click', function() {
      socket.emit('manual', { id: BOT_ID, action: 'up' });
  });

  $('#down').on('click', function() {
      socket.emit('manual', { id: BOT_ID, action: 'down' });
  });
});
