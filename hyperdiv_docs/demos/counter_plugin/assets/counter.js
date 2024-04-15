window.hyperdiv.registerPlugin("counter", (ctx) => {
  let count = 0;
  const button = document.createElement("button");
  button.innerText = "Increment";
  const countDiv = document.createElement("div");

  const updateCount = (newCount) => {
    count = newCount;
    countDiv.innerText = count;
  };

  // On click, increment the count and send the updated
  // prop value to Python:
  button.addEventListener("click", () => {
    updateCount(count + 1);
    ctx.updateProp("count", count);
  });

  // Handle incoming prop updates from Python. We ignore
  // `propValue` because there is only one prop, "count".
  ctx.onPropUpdate((propName, propValue) => {
    updateCount(propValue);
  });

  // Add the dom elements to the shadow root.
  ctx.domElement.appendChild(button);
  ctx.domElement.appendChild(countDiv);

  // Initialize the plugin with the initial count.
  updateCount(ctx.initialProps.count);
});
