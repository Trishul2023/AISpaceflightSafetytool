const socket = io();
   socket.on('update_data', function(data) {
       const tableBody = document.getElementById('data-body');
       const row = document.createElement('tr');
       row.innerHTML = `
           <td>${data.timestamp}</td>
           <td>${data.pressure}</td>
           <td>${data.oxygen}</td>
           <td>${data.radiation}</td>
           <td>${data.ai_status}</td>
           <td>${data.signal.charAt(0).toUpperCase() + data.signal.slice(1)}</td>
       `;
       tableBody.prepend(row);
       if (tableBody.children.length > 10) {
           tableBody.removeChild(tableBody.lastChild);
       }
       const signalDiv = document.getElementById('signal');
       signalDiv.className = `signal ${data.signal}`;
   });