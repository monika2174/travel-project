document.addEventListener("DOMContentLoaded", () => {
  // Featured hotels on home
  const featured = document.getElementById("featuredHotels");
  if (featured) {
    api("/api/hotels")
      .then((hotels) => {
        featured.innerHTML = hotels.slice(0, 4).map((h) => `
          <div class="col-md-6 col-lg-3">
            <div class="card hotel-card h-100">
              <img src="${h.image_url || 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600'}" class="card-img-top" alt="${h.name}">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title">${h.name}</h5>
                <p class="text-muted small mb-1"><i class="bi bi-geo-alt"></i> ${h.location || ''}</p>
                <div class="review-stars mb-2">${starsHtml(h.star_rating)}</div>
                <a href="hotel-details.html?id=${h.id}" class="btn btn-primary btn-sm mt-auto">View Details</a>
              </div>
            </div>
          </div>
        `).join("");
      })
      .catch(() => {
        featured.innerHTML = `<div class="col-12 text-center text-muted">Could not load hotels. Is the API running?</div>`;
      });
  }

  // Featured trips
  const featuredTrips = document.getElementById("featuredTrips");
  if (featuredTrips) {
    api("/api/trips")
      .then((trips) => {
        featuredTrips.innerHTML = trips.slice(0, 4).map((t) => `
          <div class="col-md-6 col-lg-3">
            <div class="card trip-card h-100">
              <img src="${t.image_url || 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=600'}" class="card-img-top" alt="${t.title}">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title">${t.title}</h5>
                <p class="text-muted small">${t.duration_days} days · From <span class="price-tag">$${t.price}</span></p>
                <a href="trip-details.html?id=${t.id}" class="btn btn-outline-primary btn-sm mt-auto">View Trip</a>
              </div>
            </div>
          </div>
        `).join("");
      })
      .catch(() => {});
  }

  // Popular destinations
  const popularDest = document.getElementById("popularDestinations");
  if (popularDest) {
    api("/api/destinations")
      .then((dests) => {
        popularDest.innerHTML = dests.slice(0, 4).map((d) => `
          <div class="col-md-6 col-lg-3">
            <div class="card dest-card h-100">
              <img src="${d.image_url || 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=600'}" class="card-img-top" alt="${d.name}">
              <div class="card-body">
                <h5 class="card-title">${d.name}</h5>
                <p class="text-muted small">${d.country}</p>
                <p class="small">${(d.description || '').substring(0, 80)}...</p>
                <a href="destinations.html" class="btn btn-sm btn-primary">Explore</a>
              </div>
            </div>
          </div>
        `).join("");
      })
      .catch(() => {});
  }

  // Hero search
  const heroSearch = document.getElementById("heroSearch");
  if (heroSearch) {
    heroSearch.addEventListener("submit", (e) => {
      e.preventDefault();
      const dest = document.getElementById("searchDest")?.value || "";
      window.location.href = `hotels.html?location=${encodeURIComponent(dest)}`;
    });
  }
});
