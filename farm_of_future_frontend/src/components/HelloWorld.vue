<template>
  <div class="farm-of-the-future-description">
    <h1>Farm of the Future</h1>
    <p>A Revolutionary Web App for Modern Agriculture</p>

    <div class="feature-wrapper">
      <h2>Feature 1: Satellite Image Overlay</h2>
      <p>Our web app displays a satellite image as an overlay on top of an interactive map, providing farmers with a bird's-eye view of their crops. Users can choose which date they would like to see, allowing them to track changes over time and make informed decisions about their farming practices.</p>
    </div>

    <div class="feature-wrapper">
      <h2>Feature 2: Sensor Data Line Graph</h2>
      <p>Our web app also displays sensor data as a line graph, currently only for soil moisture. Users can choose which depth, site, and plot they would like to see, giving them a detailed understanding of the moisture levels in their soil and helping them make data-driven decisions about irrigation and other farming practices.</p>
    </div>
    <p>If you encounter any issues with our web app, feel free to create an <a href="https://github.com/yourusername/farm-of-the-future/issues">issue on GitHub</a>.</p>
  </div>
</template>

<style>
  .farm-of-the-future-description {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
  }

  h1 {
    font-size: 3em;
    margin: 0;
    padding: 10px;
  }

  h2 {
    font-size: 2em;
    margin-top: 40px;
  }

  p {
    font-size: 1.2em;
    line-height: 1.5;
    margin-bottom: 20px;
    text-align: justify;
    text-justify: inter-word;
    padding: 10px;
  }

  .feature-wrapper {
    margin-bottom: 50px;
  }
</style>


<script>
export default {
  name: 'HelloWorld',
}
</script>
