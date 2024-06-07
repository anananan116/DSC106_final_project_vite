<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';

    export let country = "United States of America";
    export let city = "Los Angeles";
    export let index;

    let summerData = [];
    let winterData = [];
    let isVisible = false;
    let containerWidth;
    let containerHeight;

    let prevCountry;
    let prevCity;

    let tooltip;

    async function fetchSummerData() {
        try {
            console.log('Fetching summer data...');
            const response = await fetch(`https://dsc-climate-data.xyz/temperature/summer?country=${country}&city=${city}`);
            if (!response.ok) throw new Error('Network response was not ok');
            const jsonData = await response.json();
            summerData = jsonData;
            console.log('Summer data fetched:', summerData);
            renderClimateStripes();
            renderLinePlot();
        } catch (error) {
            console.error('Fetching summer data failed:', error);
        }
    }

    async function fetchWinterData() {
        try {
            console.log('Fetching winter data...');
            const response = await fetch(`https://dsc-climate-data.xyz/temperature/winter?country=${country}&city=${city}`);
            if (!response.ok) throw new Error('Network response was not ok');
            const jsonData = await response.json();
            winterData = jsonData;
            console.log('Winter data fetched:', winterData);
            renderClimateStripes();
            renderLinePlot();
        } catch (error) {
            console.error('Fetching winter data failed:', error);
        }
    }

    onMount(() => {
        fetchSummerData();
        fetchWinterData();
        adjustDimensions();
        window.addEventListener('resize', adjustDimensions);
        return () => window.removeEventListener('resize', adjustDimensions);
    });

    function adjustDimensions() {
        requestAnimationFrame(() => {
            const parent = document.getElementById('climate-stripe-container').parentElement;
            containerWidth = (parent ? parent.clientWidth : window.innerWidth) || 600; // Provide a default width
            containerHeight = window.innerHeight * 0.2 || 200; // Provide a default height
            console.log('Adjusted dimensions:', containerWidth, containerHeight);
            renderClimateStripes();
            renderLinePlot();
        });
    }

    function renderClimateStripes() {
        renderClimateStripe('summer-stripe', summerData, "Average Summer Temperature Change Compared to the Year of 1910");
        renderClimateStripe('winter-stripe', winterData, "Average Winter Temperature Change Compared to the Year of 1910");
        renderLegend();
    }

    function renderClimateStripe(id, data, title) {
        if (data.length === 0 || !containerWidth || !containerHeight) return;

        const margin = { top: 40, right: 20, bottom: 20, left: 20 };
        const width = containerWidth - margin.left - margin.right;
        const height = containerHeight - margin.top - margin.bottom;

        const svg = d3.select(`#${id}`)
            .html('') // Clear previous svg content
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Add title
        svg.append('text')
            .attr('x', width / 2)
            .attr('y', -10)
            .attr('text-anchor', 'middle')
            .style('font-size', '16px')
            .text(title);

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
            .attr('fill', d => colorScale(d.temperature))
            .on('mousemove', function (event, d) {
                const [mouseX, mouseY] = d3.pointer(event);
                const containerRect = document.getElementById(id).getBoundingClientRect();
                const yOffset = containerRect.top;
                const leftEdge = containerRect.left;
                const tooltipWidth = 300;
                console.log(window.innerWidth - 400);
                console.log(mouseX + tooltipWidth + 30);
                const xOffset = mouseX + tooltipWidth + 30 + leftEdge > window.innerWidth ? -tooltipWidth - 30 : 30;
                
                d3.select(tooltip)
                    .style('left', `${mouseX + xOffset}px`)
                    .style('top', `${mouseY + yOffset}px`)
                    .style('display', 'block')
                    .html(`
                        <strong>Country:</strong> ${country}<br>
                        <strong>City:</strong> ${city}<br>
                        <strong>Year:</strong> ${d.year}<br>
                        <strong>Temperature Change:</strong> ${d.temperature.toFixed(2)}°C
                    `);
            })
            .on('mouseout', () => {
                d3.select(tooltip).style('display', 'none');
            });
    }

    function renderLegend() {
        const margin = { top: 0, right: 20, bottom: 10, left: 20 };
        const legendWidth = containerWidth - margin.left - margin.right;
        const legendHeight = 50;

        const svg = d3.select('#legend')
            .html('') // Clear previous svg content
            .append('svg')
            .attr('width', legendWidth + margin.left + margin.right)
            .attr('height', legendHeight + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        const legendScale = d3.scaleLinear()
            .domain([-0.5, 1.5])
            .range([0, legendWidth]);

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

        const legendAxis = d3.axisBottom(legendScale)
            .tickValues([-0.5, -0.25, 0, 0.5, 1, 1.5])
            .tickFormat(d => d.toFixed(2) + "°C");

        svg.selectAll("rect")
            .data(d3.range(-0.5, 1.5, 0.01))
            .enter().append("rect")
            .attr("x", d => legendScale(d))
            .attr("y", 0)
            .attr("width", legendWidth / 200)
            .attr("height", legendHeight - 20)
            .attr("fill", d => colorScale(d));

        svg.append("g")
            .attr("transform", `translate(0, ${legendHeight - 20})`)
            .call(legendAxis);
    }

    function renderLinePlot() {
        if (summerData.length === 0 || winterData.length === 0 || !containerWidth || !containerHeight) return;

        const margin = { top: 40, right: 40, bottom: 40, left: 40 };
        const width = containerWidth - margin.left - margin.right;
        const height = 300 - margin.top - margin.bottom;

        const svg = d3.select('#line-plot')
            .html('') // Clear previous svg content
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Add title
        svg.append('text')
            .attr('x', width / 2)
            .attr('y', -20)
            .attr('text-anchor', 'middle')
            .style('font-size', '16px')
            .text('Temperature Change Over the Years');

        const years = summerData.map(d => d.year);

        const x = d3.scaleBand()
            .domain(years)
            .range([0, width])
            .padding(0.1);

        const y = d3.scaleLinear()
            .domain([d3.min([...summerData, ...winterData], d => d.temperature), d3.max([...summerData, ...winterData], d => d.temperature)])
            .range([height, 0]);

        const line = d3.line()
            .x(d => x(d.year) + x.bandwidth() / 2)
            .y(d => y(d.temperature))
            .curve(d3.curveMonotoneX);

        // Filter the years to display only one label every 10 years
        const filteredYears = years.filter(year => year % 10 === 0);

        // Add X axis
        svg.append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(d3.axisBottom(x).tickValues(filteredYears));

        // Add Y axis on the left
        svg.append('g')
            .call(d3.axisLeft(y));

        // Add Y axis on the right
        svg.append('g')
            .attr('transform', `translate(${width}, 0)`)
            .call(d3.axisRight(y));

        // Add the summer line
        svg.append('path')
            .datum(summerData)
            .attr('fill', 'none')
            .attr('stroke', 'orange')
            .attr('stroke-width', 1.5)
            .attr('d', line);

        // Add the winter line
        svg.append('path')
            .datum(winterData)
            .attr('fill', 'none')
            .attr('stroke', 'blue')
            .attr('stroke-width', 1.5)
            .attr('d', line);

        // Add points for summer data
        svg.selectAll('.dot-summer')
            .data(summerData)
            .enter()
            .append('circle')
            .attr('class', 'dot-summer')
            .attr('cx', d => x(d.year) + x.bandwidth() / 2)
            .attr('cy', d => y(d.temperature))
            .attr('r', 3)
            .attr('fill', 'orange');

        // Add points for winter data
        svg.selectAll('.dot-winter')
            .data(winterData)
            .enter()
            .append('circle')
            .attr('class', 'dot-winter')
            .attr('cx', d => x(d.year) + x.bandwidth() / 2)
            .attr('cy', d => y(d.temperature))
            .attr('r', 3)
            .attr('fill', 'blue');

        // Add legend
        const legend = svg.append('g')
            .attr('class', 'legend')
            .attr('transform', `translate(${width - 150}, ${height-80})`); // Adjust position as needed

        legend.append('rect')
            .attr('x', 0)
            .attr('y', 0)
            .attr('width', 150)
            .attr('height', 50)
            .attr('fill', 'none')
            .attr('stroke', 'black');

        legend.append('circle')
            .attr('cx', 15)
            .attr('cy', 15)
            .attr('r', 6)
            .attr('fill', 'orange');

        legend.append('text')
            .attr('x', 30)
            .attr('y', 15)
            .attr('dy', '.35em')
            .text('Summer Data')
            .style('font-size', '12px')
            .attr('alignment-baseline', 'middle');

        legend.append('circle')
            .attr('cx', 15)
            .attr('cy', 35)
            .attr('r', 6)
            .attr('fill', 'blue');

        legend.append('text')
            .attr('x', 30)
            .attr('y', 35)
            .attr('dy', '.35em')
            .text('Winter Data')
            .style('font-size', '12px')
            .attr('alignment-baseline', 'middle');
    }

    $: {
        if ((country !== prevCountry || city !== prevCity) && country && city) {
            prevCountry = country;
            prevCity = city;
            fetchSummerData();
            fetchWinterData();
        }
    }

    $: if (index === 2) {
        console.log('ClimateStripe is visible');
        isVisible = true;
        renderClimateStripes();
        renderLinePlot();
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

<div id="climate-stripe-container" style="width: 100%; display: {isVisible ? 'block' : 'none'};">
    <div id="summer-stripe" style="height: 240px;"></div>
    <div id="winter-stripe" style="height: 240px;"></div>
    <div id="legend" style="height: 60px; margin: 10px 0;"></div>
    <div id="line-plot" style="height: 340px;"></div>
</div>

<div class="tooltip" bind:this={tooltip}></div>
