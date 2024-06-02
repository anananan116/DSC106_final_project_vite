<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';

    export let country = "United States of America";
    export let city = "San Diego";
    export let index;

    let data = [];
    let isVisible = false;
    let containerWidth;
    let containerHeight;

    async function fetchData() {
        try {
            const response = await fetch(`http://dsc-climate-data.xyz/temperature/summer?country=${country}&city=${city}`);
            if (!response.ok) throw new Error('Network response was not ok');
            const jsonData = await response.json();
            data = jsonData;
            renderClimateStripe();
        } catch (error) {
            console.error('Fetching data failed:', error);
        }
    }

    onMount(() => {
        fetchData();
        adjustDimensions();
        window.addEventListener('resize', adjustDimensions);
        return () => window.removeEventListener('resize', adjustDimensions);
    });

    function adjustDimensions() {
        containerWidth = document.getElementById('climate-stripe').clientWidth;
        containerHeight = window.innerHeight * 0.2;
        renderClimateStripe();
    }

    function renderClimateStripe() {
        if (data.length === 0) return;

        const margin = { top: 20, right: 20, bottom: 20, left: 20 };
        const width = containerWidth - margin.left - margin.right;
        const height = containerHeight - margin.top - margin.bottom;

        const svg = d3.select('#climate-stripe')
            .html('') // Clear previous svg content
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
