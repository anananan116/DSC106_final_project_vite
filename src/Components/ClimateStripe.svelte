<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
  
    export let country = "United States";
    export let city = "San Diego";
    export let index;

    let data = [];
    
    let isVisible = false;
    onMount(async () => {
      const response = await fetch(`http://35.94.151.97/temperature/summer?country=${country}&city=${city}`);
      data = await response.json();
      renderClimateStripe();
    });
  
    function renderClimateStripe() {
      const margin = { top: 20, right: 20, bottom: 20, left: 20 };
      const width = 800 - margin.left - margin.right;
      const height = 50 - margin.top - margin.bottom;
  
      const svg = d3.select('#climate-stripe')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);
  
      const years = data.map(d => d.year);
      const temperatures = data.map(d => d.temperature);
  
      const x = d3.scaleBand()
        .domain(years)
        .range([0, width])
        .padding(0.01);
  
      const colorScale = d3.scaleLinear()
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
  
      svg.selectAll('.stripe')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'stripe')
        .attr('x', d => x(d.year))
        .attr('y', 0)
        .attr('width', x.bandwidth())
        .attr('height', height)
        .attr('fill', d => colorScale(d.temperature));
    }
    $: if (index === 2) {
    isVisible = true;
    } else {
    isVisible = false;
    }
  </script>
  
  <style>
    svg {
      display: block;
      margin: auto;
    }
  
    .stripe {
      shape-rendering: crispEdges;
    }
  </style>
  <div id="climate-stripe" style="width: 100%; display: {isVisible ? 'block' : 'none'};"></div>
  