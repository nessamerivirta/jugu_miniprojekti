const divFilter = document.getElementById("divfilter");
const txtError = document.getElementById("txterror");

const toggleBtn = document.getElementById("btntoggle");
const updateBtn = document.getElementById("btnupdate");

const file = document.getElementById("txtfilename").value.trim();

fetch(`/static/${encodeURIComponent(file)}`)
  .then(response => {
    if (!response.ok) throw new Error(`Could not load ${file}: ${response.status}`);
    return response.text();
  })
  .then(html => {
    divFilter.innerHTML = html;
  })
  .catch(error => {
    txtError.value = error.message;
  });

toggleBtn.addEventListener('click', () => {
    divFilter.classList.toggle('hide');
});

updateBtn.addEventListener('click', async (event) => {
    if (!(event.target instanceof Element) ||
        !event.target.closest("#btnupdate"))
    {
        return;
    }

    const filters = {
        author: {
            enabled: divFilter.querySelector("#cbauthor").checked,
            value: divFilter.querySelector("#txtauthor").value.trim()
        },
        publishing_year: {
            enabled: divFilter.querySelector("#cbpub_year").checked,
            value: divFilter.querySelector("#txtpub_year").value.trim()
        },
        title: {
            enabled: divFilter.querySelector("#cbtitle").checked,
            value: divFilter.querySelector("#txttitle").value.trim()
        }
    };

    try
    {
        const response = await fetch("/update_mainview", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(filters)
        });

        const html = await response.text();
        if (!response.ok)
        {
            throw new Error(html || `Request failed: ${response.status}`);
        }

        const updatedPage = new DOMParser().parseFromString(html, "text/html");
        const updatedResults = updatedPage.querySelector("#reference-results");
        const currentResults = document.querySelector("#reference-results");

        if (!updatedResults || !currentResults) {
            throw new Error("The response did not contain reference results.");
        }

        // Use result to update the main view.
        currentResults.replaceWith(updatedResults);
    }
    catch (error)
    {
        txtError.value = error.message;
    }

});
