const searchInput = document.getElementById("ingredientSearch");
const searchResults = document.getElementById("searchResults");
const selectedIngredients = document.getElementById("selectedIngredients");

// Function to fetch ingredients from the backend
async function searchIngredients(query) {
    if (!query.trim()) {
        searchResults.innerHTML = "";
        searchResults.classList.add("hidden");
        return;
    }

    const response = await fetch(`/ingredients/search_ingredients?query=${query}`);
    const ingredients = await response.json();

    if (ingredients.length === 0) {
        searchResults.innerHTML = "<p class='p-2 text-gray-400'>No results found</p>";
        searchResults.classList.remove("hidden");
        return;
    }

    searchResults.innerHTML = "";
    ingredients.forEach(ingredient => {
        const item = document.createElement("div");
        item.classList.add("p-2", "cursor-pointer", "hover:bg-gray-600");
        item.textContent = `${ingredient.name} (${ingredient.unit})`;
        item.onclick = () => selectIngredient(ingredient);
        searchResults.appendChild(item);
    });

    searchResults.classList.remove("hidden");
}

function selectIngredient(ingredient) {
    // Clear the search input
    document.getElementById("ingredientSearch").value = "";

    // Hide search results
    searchResults.innerHTML = "";
    searchResults.classList.add("hidden");

    // Prevent duplicate selection
    if (document.getElementById(`ingredient-${ingredient.id}`)) {
        return;
    }

    // Create new table row
    const row = document.createElement("tr");
    row.id = `ingredient-${ingredient.id}`;
    row.classList.add("border-b", "border-gray-500");

    row.innerHTML = `
        <td class="p-2">${ingredient.name}</td>
        <td class="p-2">${ingredient.unit}</td>
        <td class="p-2">
            <input type="number" min="1" class="p-1 bg-gray-800 text-white w-24 text-center amount-input"
                   placeholder="Amount" data-price="${ingredient.price}" oninput="updatePrice(${ingredient.id})">
        </td>
        <td class="p-2 price-display" id="price-${ingredient.id}">$0.00</td>
        <td class="p-2 text-center">
            <button onclick="removeIngredient(${ingredient.id})" class="text-gray-400 hover:text-gray-200">✖</button>
        </td>
    `;

    // Append row to table
    document.getElementById("selectedIngredients").appendChild(row);
}


// Function to update the price dynamically
function updatePrice(ingredientId) {
    const amountInput = document.querySelector(`#ingredient-${ingredientId} .amount-input`);
    const priceDisplay = document.getElementById(`price-${ingredientId}`);
    
    let amount = parseFloat(amountInput.value);
    let pricePerUnit = parseFloat(amountInput.dataset.price);
    
    if (!isNaN(amount) && amount > 0) {
        let totalPrice = (amount * pricePerUnit).toFixed(2);
        priceDisplay.textContent = `$${totalPrice}`;
    } else {
        priceDisplay.textContent = "$0.00";
    }
}

// Function to remove a selected ingredient
function removeIngredient(ingredientId) {
    const row = document.getElementById(`ingredient-${ingredientId}`);
    if (row) {
        row.remove();
    }
}


// Event listener for input search
searchInput.addEventListener("input", () => searchIngredients(searchInput.value));

async function saveMeal() {
    let mealName = document.getElementById('mealName').value.trim();
    let mealCategory = document.getElementById('mealCategory').value;
    let mealInstructions = document.getElementById('mealInstructions').value.trim();
    let cookTime = parseInt(document.getElementById('cookTime').value.trim()) || 0;

    // Get selected ingredients and amounts
    let selectedRows = document.querySelectorAll("#selectedIngredients tr");
    let ingredients = [];

    selectedRows.forEach(row => {
        let ingredientName = row.cells[0].innerText;
        let unit = row.cells[1].innerText;
        let amount = row.querySelector(".amount-input").value;

        if (amount && parseInt(amount) > 0) {
            ingredients.push({
                name: ingredientName,
                amount: parseInt(amount),
                unit: unit
            });
        }
    });

    // Validation
    if (!mealName || ingredients.length === 0) {
        alert("Please enter a meal name and select at least one ingredient.");
        return;
    }

    // Create payload
    let mealData = {
        name: mealName,
        ingredients: ingredients,
        category: mealCategory,
        instructions: mealInstructions,
        cook_time: cookTime
    };

    try {
        let response = await fetch("/meals/add_meal", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(mealData)
        });

        let result = await response.json();

        if (response.ok) {
            alert(`Meal '${mealName}' has been saved successfully!`);
            document.getElementById('mealName').value = '';
            document.getElementById('mealCategory').value = 'Breakfast';
            document.getElementById('mealInstructions').value = '';
            document.getElementById('cookTime').value = '';
            document.getElementById('selectedIngredients').innerHTML = ''
            window.location.reload();
        } else {
            alert(`Error: ${result.error}`);
        }

    } catch (error) {
        console.error("Error saving meal:", error);
        alert("An error occurred while saving the meal.");
    }
}

function backToMealPlannerFromCreating() {
    let mealCreationElement = document.getElementById("createMeal");
    let mealsElement = document.getElementById("mainMeals");

    if (!mealCreationElement || !mealsElement) {
        console.error("One of the elements (#createMeal or #mainMeals) is missing!");
        return;
    }

    // Step 1: Fade out createMeal
    mealCreationElement.style.transition = "opacity 1s ease-in-out";
    mealCreationElement.style.opacity = "0";

    setTimeout(() => {
        mealCreationElement.style.display = "none"; // Hide after fade-out

        // Step 2: Show mainMeals and fade it in
        mealsElement.style.display = "flex"; // Make it visible
        mealsElement.style.opacity = "0"; // Start invisible
        mealsElement.style.transition = "opacity 1s ease-in-out";

        setTimeout(() => {
            mealsElement.style.opacity = "1"; // Fade in
        }, 10); // Small delay to trigger transition
    }, 1000); // Wait for fade-out to complete
}
