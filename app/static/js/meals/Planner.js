function setMealInformation() {

    fetch("/meals/amount")
        .then(response => response.json())
        .then(data => {
            document.getElementById("totalAmountOfMeals").innerText =
                `A total of ${data.amounts[0]} meals and ${data.amounts[1]} ingredients!`;
        })
        .catch(error => console.error("Error fetching meal & ingredient amounts:", error));

}


function openCreateMeal() {
    let mealCreationElement = document.getElementById("createMeal");
    let mealsElement = document.getElementById("mainMeals");

    if (!mealCreationElement || !mealsElement) {
        console.error("One of the elements (#createMeal or #mainMeals) is missing!");
        return;
    }

    // Step 1: Fade out mainMeals
    mealsElement.style.transition = "opacity 1s ease-in-out";
    mealsElement.style.opacity = "0";

    setTimeout(() => {
        mealsElement.style.display = "none"; // Hide after fade-out

        // Step 2: Show createMeal and fade it in
        mealCreationElement.style.display = "flex"; // Make it visible
        mealCreationElement.style.opacity = "0"; // Start invisible
        mealCreationElement.style.transition = "opacity 1s ease-in-out";

        setTimeout(() => {
            mealCreationElement.style.opacity = "1"; // Fade in
        }, 10); // Small delay to trigger transition
    }, 1000); // Wait for fade-out to complete
}


function backToMain() {
    let mainElement = document.getElementById("mainScreen");
    let mealsElement = document.getElementById("mainMeals");

    if (!mainElement || !mealsElement) {
        console.error("One of the elements (#mainScreen or #mainMeals) is missing!");
        return;
    }

    // Step 1: Fade out mainMeals
    mealsElement.style.transition = "opacity 1s ease-in-out";
    mealsElement.style.opacity = "0";

    setTimeout(() => {
        mealsElement.style.display = "none"; // Hide it after fade-out

        // Step 2: Show mainScreen and fade it in
        mainElement.style.display = "flex"; // Ensure it’s visible
        mainElement.style.opacity = "0"; // Ensure it starts invisible
        mainElement.style.transition = "opacity 1s ease-in-out";

        setTimeout(() => {
            mainElement.style.opacity = "1"; // Fade in
        }, 10); // Small delay to trigger transition
    }, 1000); // Wait for fade-out to complete
}

document.addEventListener("DOMContentLoaded", function () {
    let draggedMeal = null; // Store the dragged meal

    const meals = document.querySelectorAll(".meal");
    const dropZones = document.querySelectorAll(".drop-zone");
    const trashCan = document.getElementById("trashCan");

    // ✅ Ensure mealData is properly set when dragging from the middle card
    meals.forEach(meal => {
        meal.addEventListener("dragstart", (event) => {
            const mealData = {
                name: meal.dataset.name,
                ingredients: meal.dataset.ingredients,
                id: Math.random().toString(36).substr(2, 9) // Unique ID
            };
            event.dataTransfer.setData("mealData", JSON.stringify(mealData)); // Store full data
            draggedMeal = meal; // Track dragged meal
        });
    });

    dropZones.forEach(zone => {
        zone.addEventListener("dragover", (event) => {
            event.preventDefault();
        });

        zone.addEventListener("drop", (event) => {
            event.preventDefault();

            // ✅ FIX: Ensure mealData is not empty before parsing
            const mealDataString = event.dataTransfer.getData("mealData");
            if (!mealDataString) return; // Prevents error

            const mealData = JSON.parse(mealDataString); // Parse the stored meal data

            // ✅ Ensure only 1 meal is allowed in Breakfast, Lunch, and Dinner
            if (zone.dataset.limit === "1" && zone.querySelectorAll("[data-name]").length >= 1) {
                alert("You can only add one meal here!");
                return;
            }

            // Hide the title (first h3 inside the drop zone)
            const title = zone.querySelector("h3");
            if (title) title.style.display = "none";

            // ✅ Create a unique ID for each dropped meal
            const newMeal = document.createElement("div");
            newMeal.classList.add(
                "bg-gray-700",
                "p-4",
                "rounded-md",
                "w-full",
                "text-center",
                "overflow-hidden",
                "flex",
                "items-center",
                "justify-center"
            );
            newMeal.style.height = "50px"; // Fixed height for readability
            newMeal.innerHTML = `<h3 class="font-bold">${mealData.name}</h3>`;
            newMeal.draggable = true;
            newMeal.dataset.name = mealData.name;
            newMeal.dataset.id = mealData.id; // Store unique ID

            // ✅ Store correct ID when dragging from the left card
            newMeal.addEventListener("dragstart", (event) => {
                draggedMeal = event.target; // Track dragged meal
                event.dataTransfer.setData("mealToDelete", newMeal.dataset.id);
            });

            zone.appendChild(newMeal);
        });
    });

    // ✅ Correctly remove only the dragged meal from the left card
    trashCan.addEventListener("dragover", (event) => {
        event.preventDefault();
    });

    trashCan.addEventListener("drop", (event) => {
        event.preventDefault();

        if (draggedMeal) {
            const parentZone = draggedMeal.closest(".drop-zone"); // Find the meal's section
            draggedMeal.remove(); // Remove the dragged meal

            // ✅ If the section is empty, show the title again
            if (parentZone && parentZone.querySelectorAll("[data-name]").length === 0) {
                const title = parentZone.querySelector("h3");
                if (title) title.style.display = "block";
            }

            // Reset dragged meal
            draggedMeal = null;
        }
    });
});

function openMealSection() {
    let mainElement = document.getElementById("mainScreen");
    let mealsElement = document.getElementById("mainMeals");

    if (!mainElement || !mealsElement) {
        console.error("One of the elements (#mainScreen or #mainMeals) is missing!");
        return;
    }

    // Step 1: Fade out mainScreen
    mainElement.style.transition = "opacity 1s ease-in-out";
    mainElement.style.opacity = "0";

    setTimeout(() => {
        mainElement.style.display = "none"; // Hide it after fade-out

        // Step 2: Show mainMeals and fade it in
        mealsElement.style.display = "flex"; // Ensure it’s visible
        mealsElement.style.opacity = "0"; // Ensure it starts invisible
        mealsElement.style.transition = "opacity 1s ease-in-out";

        setTimeout(() => {
            mealsElement.style.opacity = "1"; // Fade in
        }, 10); // Small delay to trigger transition
    }, 1000); // Wait for fade-out to complete
}

setMealInformation()

document.addEventListener("DOMContentLoaded", function() {
    fetch("/meals/get")
        .then(response => response.json())
        .then(data => {
            const mealsList = document.getElementById("mealsList");
            mealsList.innerHTML = "";

            data.meals.forEach(meal => {
                const ingredientCount = meal.ingredients.length;
                
                const mealDiv = document.createElement("div");
                mealDiv.classList.add("meal", "bg-gray-700", "p-4", "rounded-md", "w-5/6", "text-center", "cursor-pointer");
                mealDiv.setAttribute("draggable", "true");
                mealDiv.dataset.name = meal.name;
                mealDiv.dataset.category = meal.category;
                mealDiv.dataset.ingredients = ingredientCount;

                mealDiv.innerHTML = `
                    <h3 class="font-bold">${meal.name}</h3>
                    <p>Category: ${meal.category}</p>
                    <p>Ingredients: ${ingredientCount}</p>
                `;

                // Add drag event listener
                mealDiv.addEventListener("dragstart", (event) => {
                    event.dataTransfer.setData("mealData", JSON.stringify({
                        name: meal.name,
                        ingredients: meal.ingredients
                    }));
                });

                mealsList.appendChild(mealDiv);
            });
        })
        .catch(error => console.error("Error fetching meals:", error));
});

function openCreateIngredient() {
    let ingredientCreationElement = document.getElementById("createIngredient");
    let mealsElement = document.getElementById("mainMeals");

    if (!ingredientCreationElement || !mealsElement) {
        console.error("One of the elements (#createIngredient or #mainMeals) is missing!");
        return;
    }

    // Step 1: Fade out mainMeals
    mealsElement.style.transition = "opacity 1s ease-in-out";
    mealsElement.style.opacity = "0";

    setTimeout(() => {
        mealsElement.style.display = "none"; // Hide after fade-out

        // Step 2: Show createIngredient and fade it in
        ingredientCreationElement.style.display = "flex"; // Make it visible
        ingredientCreationElement.style.opacity = "0"; // Start invisible
        ingredientCreationElement.style.transition = "opacity 1s ease-in-out";

        setTimeout(() => {
            ingredientCreationElement.style.opacity = "1"; // Fade in
        }, 10); // Small delay to trigger transition
    }, 1000); // Wait for fade-out to complete
}
