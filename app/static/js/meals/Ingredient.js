async function saveIngredient() {
    let name = document.getElementById('ingredientName').value.trim();
    let unit = document.getElementById('ingredientUnit').value;
    let price = parseFloat(document.getElementById('ingredientPrice').value.trim());

    if (!name || isNaN(price) || price <= 0) {
        alert("Please enter a valid ingredient name and a positive price.");
        return;
    }

    // Create ingredient object
    let ingredientData = {
        name: name,
        unit: unit,
        price: price
    };

    try {
        let response = await fetch("/ingredients/add_ingredient", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(ingredientData)
        });

        let result = await response.json();

        if (response.ok) {
            alert(`Ingredient '${name}' has been saved successfully!`);
            document.getElementById('ingredientName').value = '';
            document.getElementById('ingredientUnit').value = 'g';
            document.getElementById('ingredientPrice').value = '';
            window.location.reload();
        } else {
            alert(`Error: ${result.error}`);
        }

    } catch (error) {
        console.error("Error saving ingredient:", error);
        alert("An error occurred while saving the ingredient.");
    }
}

function backToMealPlanner() {
    let ingredientCreationElement = document.getElementById("createIngredient");
    let mealsElement = document.getElementById("mainMeals");

    if (!ingredientCreationElement || !mealsElement) {
        console.error("One of the elements (#createIngredient or #mainMeals) is missing!");
        return;
    }

    // Step 1: Fade out createIngredient
    ingredientCreationElement.style.transition = "opacity 1s ease-in-out";
    ingredientCreationElement.style.opacity = "0";

    setTimeout(() => {
        ingredientCreationElement.style.display = "none"; // Hide after fade-out

        // Step 2: Show mainMeals and fade it in
        mealsElement.style.display = "flex"; // Make it visible
        mealsElement.style.opacity = "0"; // Start invisible
        mealsElement.style.transition = "opacity 1s ease-in-out";

        setTimeout(() => {
            mealsElement.style.opacity = "1"; // Fade in
        }, 10); // Small delay to trigger transition
    }, 1000); // Wait for fade-out to complete
}
