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

<section><b>Introduction</b><br>Climate change denial is still a rampant issue. Climate change, while heavily displayed in media, never seems to have easily accessible scientific data. As the timescale is larger than humans were made for, climate change has a lot of plausible deniability. This project aims to reduce that issue.<br>empty space left for videos and research</section>

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
  <section><b>Pre-industrialization</b><br>Pre-industrialization, climate change was a natural phenomina, yet occured gradually. On the right is the data of climate change before large scale human interaction. Notice how while there was a trend towards higher tempuratures, the change was much more moderate. Many of the changes occur through many "yellow" periods of small increases, instead of jumps of "red" periods.</section>
  <section><b>Current Day</b><br>Vizualised here is how we have treated the planet over the past ~100 years. We have seen historic and irreversable increases globally. "Red" periods go from being the exception to the rule. Note how even within this section of data, climate change is occuring at an increasing rate, with many of the biggest jumps in climate occuring in the past twenty years.</section>
  <section><b>Local Data</b><br>Here is the data broken down locally. Feel free to find your city to learn more about how climate change affects your local community. Many times people see climate change as a global issue, which creates a layer of abstraction between their lives and the effects of climate change. However, climate change already has and will continue to detract from all of our quality of lives.
    <div>
      <label>
        Country:
        <input type="text" bind:value={countryInput} />
      </label>
      <br>
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

<section><b>Call to Action</b><br>Action must be taken to prevent climate change before it is too late. Attached is a variety of sources from groups much more informed than we are, sorted into categories depending on what you are looking for.<br>
<br>
Individual impact:<br>
<a href="https://www.un.org/en/actnow/ten-actions">www.un.org/</a><br>
<a href="https://www.epa.gov/climate-change/what-you-can-do-about-climate-change">www.epa.gov/</a><br>
<br>
Global Trends:<br>
<a href="https://www.climate.gov/news-features/understanding-climate/climate-change-global-temperature">www.climate.gov/</a><br>
<a href="https://climate.nasa.gov/vital-signs/global-temperature/?intent=121">climate.nasa.gov/</a><br>
<br>
The Effects of Climate Change:<br>
<a href="https://www.nrdc.org/stories/what-are-effects-climate-change">www.nrdc.org/</a><br>
<a href="https://www.worldwildlife.org/threats/effects-of-climate-change">www.worldwildlife.org/</a><br>
<br>
</section>

<style>
  .background {
    margin-left: auto;
    margin-right: 0;
    height: 100vh;
    position: relative;
    z-index: 2; /* Higher z-index to ensure it is above the foreground */
  }

  .foreground {
    padding: 200x 0;
    margin-left: 0;
    margin-right: auto;
    height: auto;
    position: relative;
    font-family: 'Verdana';
    line-height: 1.8;
    font-size: 16x;
    pointer-events: auto; /* Enable pointer events for foreground */
    z-index: 1; /* Lower z-index to ensure it is below the background */
  }

  .progress-bars {
    position: absolute;
    background: rgba(170, 51, 120, 0.2) /*  40% opaque */;
    visibility: visible;
  }

  section {
    height: 80vh;
    background-color: rgba(0, 0, 0, 0); /* 20% opaque */
    /* color: white; */
    text-align: center;
    /* max-width: 750px; */
    color: black;
    padding: 1em;
    margin: 0 0 2em 0;
  }

  big-section {
    height: 80vh;
    background-color: rgba(0, 0, 0, 0); /* 20% opaque */
    /* color: white; */
    text-align: center;
    /* max-width: 750px; */
    color: black;
    padding: 1em;
    margin: 0 0 2em 0;
  }

  /* Style for the input form */
  div {
    margin: 1em 0;
  }
  label {
    margin-right: 1em;
  }
</style>
