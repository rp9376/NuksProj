// Make a GET request to the API endpoint
fetch('http://localhost:8000/menus/')
    .then(response => response.json())
    .then(data => {
        // Process the response data
        const menuContainer = document.getElementById('menu');

        // Loop through each menu item and display it
        data.forEach(week => {
            const weekInfo = document.createElement('h2');
            weekInfo.textContent = week.week_info;
            menuContainer.appendChild(weekInfo);

            week.days.forEach(day => {
                const dayInfo = document.createElement('h3');
                dayInfo.textContent = day.day;
                menuContainer.appendChild(dayInfo);

                const itemList = document.createElement('ul');
                day.items.forEach(item => {
                    const listItem = document.createElement('li');
                    listItem.textContent = item;
                    itemList.appendChild(listItem);
                });
                menuContainer.appendChild(itemList);
            });
        });
    })
    .catch(error => console.error('Error fetching menu:', error));
