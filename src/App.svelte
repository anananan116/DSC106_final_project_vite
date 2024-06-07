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
    country = countryInput;
    city = cityInput;
  }

  let countryInput = country;
  let cityInput = city;
</script>

<section class="intro">
  <h1>Motivation</h1>
  <p>Climate change denial remains a significant issue. Despite extensive media coverage, scientific data on climate change is often inaccessible and hard to understand. The long timescale of climate change creates a sense of plausible deniability. This project aims to bridge that gap by providing clear, accessible data to illustrate the reality of climate change.</p>
  <section class="hook">  
    <iframe class="video" src="https://www.youtube.com/embed/qXLqoFHGmv0"></iframe>
    <iframe class="video" src="https://www.youtube.com/embed/Uf7vYkX-WVs"></iframe>
    <iframe class="video" src="https://www.youtube.com/embed/42xHuSmwYa4"></iframe>
  </section>
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
      <p>Before industrialization, climate change was a natural phenomenon that occurred gradually. The data on the right shows the climate trends before large-scale human activity. Notice how temperature changes were moderate, with many "yellow" periods of small increases rather than sharp "red" jumps.</p>
    </section>
    <section>
      <h2>Current Day</h2>
      <p>Over the past century, human activities have led to unprecedented and irreversible global temperature increases. "Red" periods, once rare, have become common. The data on the right highlights how climate change has accelerated, especially in the past twenty years, with significant jumps in global temperatures.</p>
    </section>
    <section>
      <h2>Local Data</h2>
      <p>Climate change affects us all locally. Here, you can explore data specific to your city to understand its impact on your community. Many people perceive climate change as a distant global issue, creating a layer of abstraction between their lives and its effects. However, climate change directly impacts our daily lives, and understanding its local effects is crucial.</p>
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

<section class="outro">
  <h1>What can I do?</h1>
  <p-gap>Preventing climate change requires immediate action. Here are resources from authoritative groups, categorized to help you find the information you need to make a difference.</p-gap>
  <section class="outro-research">  
    <div class="links">
      <h3>Individual impact:</h3>
      <a href="https://www.un.org/en/actnow/ten-actions" class="hyperlinks">www.un.org</a>
      <a href="https://www.epa.gov/climate-change/what-you-can-do-about-climate-change" class="hyperlinks">www.epa.gov</a>
      
      <h3>Global Trends:</h3>
      <a href="https://www.climate.gov/news-features/understanding-climate/climate-change-global-temperature" class="hyperlinks">www.climate.gov</a>
      <a href="https://climate.nasa.gov/vital-signs/global-temperature/?intent=121" class="hyperlinks">climate.nasa.gov</a>
      
      <h3>The Effects of Climate Change:</h3>
      <a href="https://www.nrdc.org/stories/what-are-effects-climate-change" class="hyperlinks">www.nrdc.org</a>
      <a href="https://www.worldwildlife.org/threats/effects-of-climate-change" class="hyperlinks">www.worldwildlife.org</a>
    </div>
    <div class="links">
      <iframe class="video" src="https://www.youtube.com/embed/fw01_q0cxM8"></iframe>
      <iframe class="video" src="https://www.youtube.com/embed/xZZNM3Dib0o"></iframe>
    </div>
  </section>
</section>

<style>
  .hyperlinks {
    font-size: 1.25em;
  }

  body {
    font-family: 'Verdana', sans-serif;
    line-height: 1.6;
    color: #333;
    margin: 0;
    padding: 0;
  }

  .hook {
    height: 50vh;
    display: flex;
    flex-direction: row;
    gap: 20px;
  }

  .video {
    display: inline-block;
    height: 28.12vh;
    width: 50vh;
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

  p-gap {
    max-width: 800px;
    font-size: 1.2em;
    margin-bottom: 1em;
    line-height: 1.8;
    row-gap: 30px;
    padding-bottom: 30px;
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

  div {
    margin: 1em 0;
  }

  label {
    margin-right: 1em;
  }

  outro {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2em;
  }

  .outro-research {
    height: 50vh;
    display: flex;
    flex-direction: row;
    gap: 20px;
  }

  .outro-embeds {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
</style>
