<script>
  import Scroller from "./Components/Scroller.svelte";
  import Map from "./Components/Map.svelte";
  import ClimateStripe from "./Components/ClimateStripe.svelte";

  let count, index, offset, progress;
  let width, height;
  let currentYear = 1880;

  let geoJsonToFit = {
    type: "FeatureCollection",
    features: [
      {
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [1, 0],
        },
      },
      {
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: [0, 1],
        },
      },
    ],
  };

  let country = "United States of America";
  let city = "San Diego";

  function updateClimateStripe() {
    // Update the ClimateStripe component by re-binding the country and city variables
    country = countryInput;
    city = cityInput;
  }

  let countryInput = country;
  let cityInput = city;
</script>

<section class="intro">
  <h1>Introduction</h1>
  <p>Climate change denial is still a rampant issue. Climate change, while heavily displayed in media, never seems to have easily accessible scientific data. As the timescale is larger than humans were made for, climate change has a lot of plausible deniability. This project aims to reduce that issue.</p>
  <iframe width="420" height="345" src="https://www.youtube.com/watch?v=qXLqoFHGmv0"></iframe>
</section>

<Scroller
  top={0.0}
  bottom={1}
  threshold={0.5}
  bind:count
  bind:index
  bind:offset
  bind:progress
>
  <div class="foreground" slot="foreground" style="pointer-events: auto;">
    <section>
      <h2>Pre-industrialization</h2>
      <p>Pre-industrialization, climate change was a natural phenomenon, yet occurred gradually. On the right is the data of climate change before large scale human interaction. Notice how while there was a trend towards higher temperatures, the change was much more moderate. Many of the changes occur through many "yellow" periods of small increases, instead of jumps of "red" periods.</p>
    </section>
    <section>
      <h2>Current Day</h2>
      <p>Visualized here is how we have treated the planet over the past ~100 years. We have seen historic and irreversible increases globally. "Red" periods go from being the exception to the rule. Note how even within this section of data, climate change is occurring at an increasing rate, with many of the biggest jumps in climate occurring in the past twenty years.</p>
    </section>
    <section>
      <h2>Local Data</h2>
      <p>Here is the data broken down locally. Feel free to find your city to learn more about how climate change affects your local community. Many times people see climate change as a global issue, which creates a layer of abstraction between their lives and the effects of climate change. However, climate change already has and will continue to detract from all of our quality of lives.</p>
      <div class="form">
        <label>
          Country:
          <input type="text" bind:value={countryInput} />
        </label>
        <label>
          City:
          <input type="text" bind:value={cityInput} />
        </label>
        <button on:click={updateClimateStripe}>Update</button>
      </div>
    </section>
  </div>

  <div
    class="background"
    slot="background"
    bind:clientWidth={width}
    bind:clientHeight={height}
  >
    <Map {index} {currentYear} />
    <ClimateStripe {index} {country} {city} />
  </div>
</Scroller>

<section class="cta">
  <h1>Call to Action</h1>
  <p>Action must be taken to prevent climate change before it is too late. Attached is a variety of sources from groups much more informed than we are, sorted into categories depending on what you are looking for.</p>
  <div class="links">
    <h3>Individual impact:</h3>
    <a href="https://www.un.org/en/actnow/ten-actions">www.un.org</a>
    <a href="https://www.epa.gov/climate-change/what-you-can-do-about-climate-change">www.epa.gov</a>
    
    <h3>Global Trends:</h3>
    <a href="https://www.climate.gov/news-features/understanding-climate/climate-change-global-temperature">www.climate.gov</a>
    <a href="https://climate.nasa.gov/vital-signs/global-temperature/?intent=121">climate.nasa.gov</a>
    
    <h3>The Effects of Climate Change:</h3>
    <a href="https://www.nrdc.org/stories/what-are-effects-climate-change">www.nrdc.org</a>
    <a href="https://www.worldwildlife.org/threats/effects-of-climate-change">www.worldwildlife.org</a>
  </div>
</section>

<style>
  body {
    font-family: 'Verdana', sans-serif;
    line-height: 1.6;
    color: #333;
    margin: 0;
    padding: 0;
  }

  .intro, .cta, section {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2em;
  }

  h1 {
    font-size: 2.5em;
    margin-bottom: 0.5em;
    color: #2c3e50;
  }

  h2 {
    font-size: 2em;
    margin-bottom: 0.5em;
    color: #2980b9;
  }

  h3 {
    font-size: 1.5em;
    margin-top: 1em;
    color: #27ae60;
  }

  p {
    max-width: 800px;
    font-size: 1.2em;
    margin-bottom: 1em;
    line-height: 1.8;
  }

  .placeholder {
    font-style: italic;
    color: #7f8c8d;
  }

  .form {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 1em;
  }

  label {
    margin-bottom: 0.5em;
  }

  input {
    padding: 0.5em;
    font-size: 1em;
    margin-bottom: 0.5em;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  button {
    padding: 0.5em 1em;
    font-size: 1em;
    color: white;
    background-color: #e74c3c;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  button:hover {
    background-color: #c0392b;
  }

  .links {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  a {
    color: #2980b9;
    text-decoration: none;
    margin-bottom: 0.5em;
  }

  a:hover {
    text-decoration: underline;
  }

  .background {
    margin-left: auto;
    margin-right: 0;
    height: 100vh;
    position: relative;
    z-index: 2;
  }

  .foreground {
    margin-left: 0;
    margin-right: auto;
    height: auto;
    position: relative;
    font-family: 'Verdana';
    line-height: 1.8;
    font-size: 16px;
    pointer-events: auto;
    z-index: 1;
  }

  .progress-bars {
    position: absolute;
    background: rgba(170, 51, 120, 0.2);
    visibility: visible;
  }

  section {
    height: 100vh;
    background-color: rgba(0, 0, 0, 0);
    text-align: center;
    color: black;
    padding: 1em;
    margin: 0;
  }

  /* Style for the input form */
  div {
    margin: 1em 0;
  }

  label {
    margin-right: 1em;
  }
</style>
