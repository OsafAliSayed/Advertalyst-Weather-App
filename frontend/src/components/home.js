import './home.css'
import React, { useState, useEffect } from 'react';
const Home = () => {
    var KEY = '192e3aaf21ff4c0eaab95337240503';
    var url = `https://api.weatherapi.com/v1/current.json?key=${KEY}&q=Paris`
    const [weather, setWeather] = useState({});
    fetch(url)
    .then(response => response.json())
    .then(data => setWeather(data))
    // console.log(weather)
    return (
        <div className='home card-holder'> 
            <div className='card'>
                <h1>{weather.location.name}, {weather.location.country}</h1>
            </div>
        </div>    
    )
}

export default Home;