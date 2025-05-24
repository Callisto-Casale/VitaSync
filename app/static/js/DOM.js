document.addEventListener('DOMContentLoaded', function () {

    function updateTemperature() {
        fetch('/api/temp')
            .then(response => response.json())
            .then(data => {
                document.getElementById('temperature').innerText = data.temperature;
            });
    }

    function reloadPage() {
        fetch('/reload', {
                method: 'POST'
            })
            .then(response => {
                if (response.ok) {
                    console.log("Reload triggered successfully.");
                    location.reload();
                } else {
                    console.error("Failed to trigger reload.");
                }
            })
            .catch(error => console.error("Error:", error));
    }

    function updateRAM() {
        fetch('/api/ram')
            .then(response => response.json())
            .then(data => {
                document.getElementById('ram-usage').innerText = data.ram_usage;
            });
    }

    function updateDisk() {
        fetch('/api/disk')
            .then(response => response.json())
            .then(data => {
                document.getElementById('disk-usage').innerText = data.disk_usage;
            });
    }

    function updateSystemUptime() {
        fetch('/api/uptime')
            .then(response => response.json())
            .then(data => {
                document.getElementById('system-uptime').innerText = data.uptime;
            });
    }

    function updateNetwork() {
        fetch('/api/network')
            .then(response => response.json())
            .then(data => {
                document.getElementById('ip-address').innerText = data.ip_address;
                document.getElementById('wifi-ssid').innerText = data.wifi_ssid;
            });
    }

    function updatePiHoleStats() {
        fetch("/pihole/stats")
            .then(response => response.json())
            .then(data => {
                let stats = data.data;
                // Custom number formatter for dot separators (German-style)
                let formatter = new Intl.NumberFormat("de-DE");

                // Format numbers
                let totalQueries = formatter.format(stats["dns_queries_today"]);
                let blockedQueries = formatter.format(stats["ads_blocked_today"]);
                let percentageBlocked = stats["ads_percentage_today"].toFixed(2) + "%";
                let domainsBlocked = formatter.format(stats["domains_being_blocked"]);
                let uniqueDomains = stats["unique_domains"];
                let uniqueDevices = stats["unique_clients"];

                // Update elements in HTML
                document.getElementById("dns_queries").innerText = totalQueries;
                document.getElementById("dns_queries_blocked").innerText = blockedQueries;
                document.getElementById("percentage_blocked").innerText = percentageBlocked;
                document.getElementById("blocked_domain_amount").innerText = domainsBlocked;
                document.getElementById("unique_domains").innerText = uniqueDomains;
                document.getElementById("unique_devices").innerText = uniqueDevices;

            })
            .catch(error => console.error("Error fetching data:", error));
    }

    setInterval(updateTemperature, 5000);
    setInterval(updateRAM, 20000);
    setInterval(updateDisk, 120000);
    setInterval(updateSystemUptime, 60000);
    setInterval(updatePiHoleStats, 10000);

    updatePiHoleStats();
    updateDisk();
    updateRAM();
    updateTemperature();
    updateNetwork();
    updateSystemUptime();


    const toggle = document.getElementById("piholeToggle");
    const statusText = document.getElementById("status");
    const piholeTitle = document.getElementById("piholeTitle");

    if (!toggle || !statusText || !piholeTitle) {
        console.error("One or more elements are missing!");
        return;
    }

    async function fetchPiHoleStatus() {
        try {
            const response = await fetch("/pihole/status");
            const data = await response.json();
            console.log(data);

            if (data.status === "enabled") {
                toggle.checked = true;
                statusText.textContent = "Enabled";
                piholeTitle.classList.remove("text-red-400");
                piholeTitle.classList.add("text-green-400");
            } else {
                toggle.checked = false;
                statusText.textContent = "Disabled";
                piholeTitle.classList.remove("text-green-400");
                piholeTitle.classList.add("text-red-400");
            }
        } catch (error) {
            console.error("Error fetching Pi-hole status:", error);
        }
    }

    fetchPiHoleStatus();

    toggle.addEventListener("change", async function () {
        const action = this.checked ? "enable" : "disable";
        try {
            const response = await fetch(`/pihole/${action}`, {
                method: "POST"
            });

            if (!response.ok) {
                console.log("Something went wrong", response);
                alert("Failed to update Pi-hole status.");
                this.checked = !this.checked;
                return;
            }

            statusText.textContent = this.checked ? "Enabled" : "Disabled";
            piholeTitle.classList.toggle("text-green-400", this.checked);
            piholeTitle.classList.toggle("text-red-400", !this.checked);

        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while updating Pi-hole status.");
            this.checked = !this.checked;
        }
    });
});
