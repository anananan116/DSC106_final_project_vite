<script>
  import { onMount, onDestroy } from 'svelte';
  import * as d3 from 'd3';
  import 'd3-scale-chromatic';
  import { writable } from 'svelte/store';
  export let index;
  export let currentYear = 1800;
  let width = 900;
  let height = 450;
  const timer = writable(null);
  let dataTime;
  let dataTime_winter = new Map();
  let dataTime_summer = new Map();
  let season = 'winter';
  let svg;
  let topo;
  let colorScale;
  let path;
  let start_year = 1880;
  let end_year = 2013;
  let season_bool;
  let isPlaying = true;
  let tooltip;
  let currentData = null;
  let currentMouseX = 0;
  let currentMouseY = 0;

  async function fetchData() {
    const responses = await Promise.all([
      fetch("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson"),
      fetch("https://raw.githubusercontent.com/anananan116/interactive_temperature_map/main/data/winter.json"),
      fetch("https://raw.githubusercontent.com/anananan116/interactive_temperature_map/main/data/summer.json"),
    ]);
    const [topoData, winterData, summerData] = await Promise.all(responses.map(res => res.json()));
    winterData.forEach(data => {
      dataTime_winter.set(data.year, data.values);
    });
    summerData.forEach(data => {
      dataTime_summer.set(data.year, data.values);
    });
    topo = topoData;
    dataTime = dataTime_winter;
  }

  function resize() {
    const parent = document.getElementById("map-container").parentElement;
    width = (parent ? parent.clientWidth : window.innerWidth) || 600;
    height = width / 2; // Maintain the aspect ratio

    // Set the SVG viewbox
    svg.attr('viewBox', `0 0 ${width} ${height}`);

    const scale = width / 7;  // Adjust based on your map's needs
    const projection = d3.geoMercator()
        .scale(scale)
        .center([0, 20])
        .translate([width / 2, height / 2]);

    path = d3.geoPath().projection(projection);
    update(currentYear);

    // Set the slider width dynamically
    const slider = document.getElementById('year-slider');
    if (slider) {
        slider.style.width = `${width - 180}px`;
    }
  }

  onMount(async () => {
    svg = d3.select("#my_dataviz");
    const projection = d3.geoMercator().scale(130).center([0, 20]).translate([width / 2, height / 2]);
    path = d3.geoPath().projection(projection);
    colorScale = d3.scaleLinear()
      .domain([-0.5, -0.25, 0, 0.5, 1, 1.5])
      .range([
          "rgb(51, 160, 255)",  // Corresponds to index 0
          "rgb(153, 222, 255)", // Corresponds to index 0.32
          "rgb(240, 240, 240)", // White transition at index 0.325
          "rgb(255, 208, 51)",  // Yellow at index 0.33
          "orange",             // Orange at index 0.66
          "red"                 // Red at index 1
      ])
      .interpolate(d3.interpolateRgb); // Use RGB interpolation for smooth color transitions
    await fetchData();
    update(currentYear);

    // Add legend
    var legend = svg.append("g")
      .attr("class", "legend")
      .attr("transform", "translate(20, 290)");

    legend.append("text")
      .attr("x", 0)
      .attr("y", 0)
      .attr("dy", ".35em")
      .style("font-weight", "bold")
      .text("Temperature Change");

    var legendData = [-0.5, -0.25, 0.0, 0.5, 1.0, 1.5];
    var legendWidth = 20;
    var legendHeight = 20;
    legend.selectAll("rect")
      .data(legendData)
      .enter().append("rect")
      .attr("x", 0)
      .attr("y", function(d, i) { return i * legendHeight + 20; }) // Adjust y position for the title
      .attr("width", legendWidth)
      .attr("height", legendHeight)
      .style("fill", function(d) { return colorScale(d); });

    legend.selectAll("text.label")
      .data(legendData)
      .enter().append("text")
      .attr("class", "label")
      .attr("x", legendWidth + 5)
      .attr("y", function(d, i) { return i * legendHeight + legendHeight / 2 + 20; }) // Adjust y position for the title
      .attr("dy", ".35em")
      .text(function(d) { return d.toFixed(2) + "°C"; });

    if (typeof window !== 'undefined') {
      window.addEventListener('resize', resize);
      resize();
    }
  });

  onDestroy(() => {
    if (typeof window !== 'undefined') {
      window.removeEventListener('resize', resize);
    }
    if (timer) {
      clearInterval(timer);
    }
  });

  function togglePlay() {
    if (isPlaying) {
      stop_timer();
      isPlaying = false;
    } else {
      create_timer();
      isPlaying = true;
    }
  }

  function create_timer() {
    timer.set(setInterval(() => {
      if (currentYear >= end_year) {
        currentYear = start_year;
      } else {
        currentYear += 1;
      }
      update(currentYear);
    }, 50));
  }

  function stop_timer() {
    timer.update(t => {
      clearInterval(t);
      return null;
    });
  }

  function switch_season() {
    if (season === 'winter') {
      dataTime = dataTime_winter;
    } else {
      dataTime = dataTime_summer;
    }
    update(currentYear);
  }
  create_timer();

  $: if (index === 0) {
    isVisible = true;
    clearInterval(timer);
    start_year = 1800;
    end_year = 1880;
    currentYear = start_year;
  } else if (index === 1) {
    isVisible = true;
    clearInterval(timer);
    start_year = 1920;
    end_year = 2013;
    currentYear = start_year;
  } else {
    if (timer){
      clearInterval(timer);
    }
    isVisible = false;
  }

  $: season, switch_season();
  
  function updateTooltip() {
    if (currentData) {
        const containerRect = document.getElementById('map-container').getBoundingClientRect();
        const yOffset = containerRect.top;
        const leftEdge = containerRect.left;
        const tooltipWidth = 300; // Adjust this value based on your tooltip width
        const xOffset = currentMouseX + tooltipWidth + 30 + leftEdge > window.innerWidth ? -tooltipWidth - 30 : 30;

        const countryName = currentData.properties.name; // Adjust this based on your GeoJSON structure

        d3.select(tooltip)
            .style('left', `${currentMouseX + xOffset}px`)
            .style('top', `${currentMouseY + yOffset}px`)
            .style('display', 'block')
            .html(`
                <strong>Country:</strong> ${countryName}<br>
                <strong>Year:</strong> ${currentYear}<br>
                <strong>Season:</strong> ${season}<br>
                <strong>Temperature Change:</strong> ${(dataTime.get(currentYear)?.[currentData.id] || 0).toFixed(2)}°C
            `);
    }
  }
  
  function update(year) {
    currentYear = year;
    if (!svg || !topo) return;
    svg.selectAll(".country")
        .data(topo.features)
        .join("path")
        .attr("class", "country")
        .attr("d", path)
        .attr("fill", d => {
            const value = dataTime.get(currentYear)?.[d.id] || 0;
            return colorScale(value);
        })
        .on('mousemove', function (event, d) {
            currentData = d;
            const [mouseX, mouseY] = d3.pointer(event);
            currentMouseX = mouseX;
            currentMouseY = mouseY;

            const containerRect = document.getElementById('map-container').getBoundingClientRect();
            const yOffset = containerRect.top;
            const leftEdge = containerRect.left;
            const tooltipWidth = 300; // Adjust this value based on your tooltip width
            const xOffset = mouseX + tooltipWidth + 30 + leftEdge > window.innerWidth ? -tooltipWidth - 30 : 30;

            const countryName = d.properties.name; // Adjust this based on your GeoJSON structure

            d3.select(tooltip)
                .style('left', `${mouseX + xOffset}px`)
                .style('top', `${mouseY + yOffset}px`)
                .style('display', 'block')
                .html(`
                    <strong>Country:</strong> ${countryName}<br>
                    <strong>Year:</strong> ${currentYear}<br>
                    <strong>Season:</strong> ${season}<br>
                    <strong>Temperature Change:</strong> ${(dataTime.get(currentYear)?.[d.id] || 0).toFixed(2)}°C
                `);
        })
        .on('mouseout', () => {
            d3.select(tooltip).style('display', 'none');
            currentData = null;
        });
        updateTooltip();
  }
  let isVisible = false;
</script>

<div id="map-container" style="width: 100%; display: {isVisible ? 'block' : 'none'};">
  <h2>Average Temperature Change Compared to the Year of 1910</h2>
  <svg id="my_dataviz"></svg>

  <div id="controls-container" style="width: 100%; display: flex; flex-direction: column; align-items: center;">
    <div style="width: 100%; display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
      <button class="control-button" on:click={togglePlay}>{isPlaying ? 'Pause' : 'Play'}</button>
      <div class="switch-container">
        <label>Winter</label>
        <label class="switch">
          <input type="checkbox" bind:checked={season_bool} on:change={() => season = season === 'winter' ? 'summer' : 'winter'}>
          <span class={season === 'winter' ? 'slider winter' : 'slider summer'}></span>
        </label>
        <label>Summer</label>
      </div>
    </div>
    <div id="slider-wrapper" style="width: 100%; display: flex; align-items: center; justify-content: space-between;">
      <span>1800</span>
      <input type="range" id="year-slider" min="1800" max="2012" step="1" bind:value={currentYear} on:input={e => update(+e.target.value)} style="flex-grow: 1; margin: 0 10px;">
      <span>2012</span>
    </div>
    <span>{currentYear}</span>
    <p class="season-note">Use the switch to toggle between summer and winter data.</p>
  </div>
</div>

<div class="tooltip" bind:this={tooltip}></div>

<style>
  #map-container {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh; /* Adjust the height as needed */
  }

  .control-button {
    background-color: #4CAF50;
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s;
  }

  .control-button:hover {
    background-color: #45a049;
  }

  #year-slider {
    width: 100%;
  }

  .slider-container {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 10px;
  }

  .switch-container {
    display: flex;
    align-items: center;
  }

  .switch {
    position: relative;
    display: inline-block;
    width: 50px;
    height: 28px;
    margin: 0 10px;
  }

  .switch input {
    opacity: 0;
    width: 0;
    height: 0;
  }

  .slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #2196F3;
    transition: .4s;
    border-radius: 34px;
  }

  .slider:before {
    position: absolute;
    content: "";
    height: 20px;
    width: 20px;
    left: 4px;
    bottom: 4px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
  }

  input:checked + .slider {
    background-color: #FF6347; /* Tomato red for Summer */
  }

  input:checked + .slider:before {
    transform: translateX(22px);
  }

  .season-note {
    font-size: 14px;
    margin-top: 10px;
  }

  .tooltip {
    position: absolute;
    padding: 10px;
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
    border-radius: 5px;
    pointer-events: none;
    display: none;
  }
</style>
