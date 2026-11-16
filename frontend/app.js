const listings = [
  {id:1,title:"Bright and spacious student hostel",type:"Hostel",price:280000,period:"year",area:"Akoka, Yaba",university:"University of Lagos",rooms:"Shared room",features:["Water supply","24/7 power","Security"],image:"https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&w=900&q=85",description:"A comfortable student hostel in a convenient location, with easy access to campus and nearby shops."},
  {id:2,title:"Modern self-contained room",type:"Self-contained",price:650000,period:"year",area:"Yaba, Lagos",university:"University of Lagos",rooms:"Private room",features:["Private bathroom","Kitchenette","Wardrobe"],image:"https://images.unsplash.com/photo-1616486338812-3dadae4b4ace?auto=format&fit=crop&w=900&q=85",description:"A neat private space with a calm interior, suitable for a student who prefers extra privacy."},
  {id:3,title:"Affordable shared apartment",type:"Shared apartment",price:420000,period:"year",area:"Ojo, Lagos",university:"Lagos State University",rooms:"Shared apartment",features:["Furnished","Water supply","Good access road"],image:"https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=900&q=85",description:"Share a well-kept apartment and split the cost while staying close to the student community."},
  {id:4,title:"Private room close to campus",type:"Single room",price:350000,period:"year",area:"Nsukka, Enugu",university:"University of Nigeria, Nsukka",rooms:"Single room",features:["Water supply","Wardrobe","Secure compound"],image:"https://images.unsplash.com/photo-1598928506311-c55ded91a20c?auto=format&fit=crop&w=900&q=85",description:"A simple, tidy room in a student-friendly neighbourhood with useful amenities nearby."},
  {id:5,title:"Private student lodge",type:"Hostel",price:190000,period:"year",area:"Akurba, Makurdi",university:"Benue State University",rooms:"Shared room",features:["Study area","Water supply","Security"],image:"https://images.unsplash.com/photo-1595576508898-0ad5c879a061?auto=format&fit=crop&w=900&q=85",description:"Budget-friendly student accommodation with a welcoming shared environment."},
  {id:6,title:"Clean mini flat for students",type:"Self-contained",price:780000,period:"year",area:"Ilishan-Remo, Ogun",university:"Babcock University",rooms:"Private apartment",features:["Private kitchen","Private bathroom","Parking"],image:"https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=900&q=85",description:"A bright mini flat with a private kitchen and bathroom in a quiet neighbourhood."},
  {id:7,title:"Comfortable shared student space",type:"Shared apartment",price:300000,period:"year",area:"Ile-Ife, Osun",university:"Obafemi Awolowo University",rooms:"Shared apartment",features:["Furnished","Laundry area","Water supply"],image:"https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=900&q=85",description:"A friendly shared apartment with practical facilities and access to the campus area."},
  {id:8,title:"Neat single room in a quiet area",type:"Single room",price:240000,period:"year",area:"Gidan Kwano, Minna",university:"Federal University of Technology, Minna",rooms:"Single room",features:["Water supply","Secure compound","Good ventilation"],image:"https://images.unsplash.com/photo-1615874694520-474822394e73?auto=format&fit=crop&w=900&q=85",description:"A simple and affordable room in a peaceful area close to student essentials."}
];

const grid = document.getElementById("listingGrid");
const universityInput = document.getElementById("universitySearch");
const areaInput = document.getElementById("areaSearch");
const typeSelect = document.getElementById("typeFilter");
const sortSelect = document.getElementById("sortSelect");
const minPriceInput = document.getElementById("minPrice");
const maxPriceInput = document.getElementById("maxPrice");
const amenitySelect = document.getElementById("amenityFilter");
const resultCount = document.getElementById("resultCount");
const emptyState = document.getElementById("emptyState");
const activeFilters = document.getElementById("activeFilters");
const dialog = document.getElementById("listingDialog");
const dialogContent = document.getElementById("dialogContent");
const saved = new Set();

function money(value) {
  return new Intl.NumberFormat("en-NG", {style:"currency",currency:"NGN",maximumFractionDigits:0}).format(value);
}
function cardTemplate(item) {
  return `<article class="listing-card" data-id="${item.id}" tabindex="0" aria-label="View ${item.title}">
    <div class="listing-photo"><img src="${item.image}" alt="${item.title}" loading="lazy"><span class="listing-tag">${item.type}</span><button class="favorite-btn ${saved.has(item.id)?"saved":""}" data-favorite="${item.id}" aria-label="Save listing">${saved.has(item.id)?"♥":"♡"}</button></div>
    <div class="listing-info"><div class="listing-location">⌖ ${item.area}</div><h3>${item.title}</h3><div class="listing-price">${money(item.price)} <small>/ year</small></div><div class="listing-meta"><span>⌂ ${item.rooms}</span><span>✓ Student-friendly</span></div></div>
  </article>`;
}
function currentResults() {
  const university = universityInput.value.trim().toLowerCase();
  const area = areaInput.value.trim().toLowerCase();
  const type = typeSelect.value;
  let results = listings.filter(item =>
    (!university || item.university.toLowerCase().includes(university)) &&
    (!area || item.area.toLowerCase().includes(area)) &&
    (!type || item.type === type) &&
    (!minPriceInput.value || item.price >= Number(minPriceInput.value)) &&
    (!maxPriceInput.value || item.price <= Number(maxPriceInput.value)) &&
    (!amenitySelect.value || item.features.includes(amenitySelect.value))
  );
  if (sortSelect.value === "low") results.sort((a,b)=>a.price-b.price);
  if (sortSelect.value === "high") results.sort((a,b)=>b.price-a.price);
  return results;
}
function renderListings() {
  const results = currentResults();
  grid.innerHTML = results.map(cardTemplate).join("");
  resultCount.textContent = `${results.length} ${results.length === 1 ? "space" : "spaces"} found`;
  emptyState.hidden = results.length > 0;
  activeFilters.innerHTML = [
    universityInput.value.trim() ? `<button class="filter-chip" data-clear="university">Campus: ${universityInput.value.trim()} ×</button>` : "",
    areaInput.value.trim() ? `<button class="filter-chip" data-clear="area">Area: ${areaInput.value.trim()} ×</button>` : "",
    typeSelect.value ? `<button class="filter-chip" data-clear="type">${typeSelect.value} ×</button>` : "",
    minPriceInput.value ? `<button class="filter-chip" data-clear="min">Min ₦${Number(minPriceInput.value).toLocaleString("en-NG")} ×</button>` : "",
    maxPriceInput.value ? `<button class="filter-chip" data-clear="max">Max ₦${Number(maxPriceInput.value).toLocaleString("en-NG")} ×</button>` : "",
    amenitySelect.value ? `<button class="filter-chip" data-clear="amenity">${amenitySelect.value} ×</button>` : ""
  ].join("");
}
function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  window.setTimeout(()=>toast.classList.remove("show"),2400);
}
function openListing(id) {
  const item = listings.find(listing=>listing.id===id);
  if (!item) return;
  dialogContent.innerHTML = `<img class="dialog-photo" src="${item.image}" alt="${item.title}"><div class="dialog-body"><div class="eyebrow">${item.type.toUpperCase()} · ${item.university}</div><h2>${item.title}</h2><div class="listing-price">${money(item.price)} <small>/ year</small></div><p>⌖ ${item.area}</p><p>${item.description}</p><div class="dialog-facts">${item.features.map(feature=>`<span>✓ ${feature}</span>`).join("")}</div><div class="dialog-actions"><a class="button button-dark" href="mailto:hello@campusnest.ng?subject=${encodeURIComponent("Enquiry: "+item.title)}">Enquire about this space ↗</a><button class="button button-outline" data-dialog-save="${item.id}">${saved.has(item.id)?"♥ Saved":"♡ Save space"}</button></div></div>`;
  dialog.showModal();
}
document.getElementById("searchBtn").addEventListener("click",()=>{renderListings();document.getElementById("listings").scrollIntoView({behavior:"smooth"});});
[universityInput,areaInput].forEach(input=>input.addEventListener("keydown",event=>{if(event.key==="Enter"){renderListings();document.getElementById("listings").scrollIntoView({behavior:"smooth"});}}));
typeSelect.addEventListener("change",renderListings);
sortSelect.addEventListener("change",renderListings);
[minPriceInput,maxPriceInput].forEach(input=>input.addEventListener("input",renderListings));
amenitySelect.addEventListener("change",renderListings);
document.getElementById("clearAllFilters").addEventListener("click",()=>{universityInput.value="";areaInput.value="";typeSelect.value="";minPriceInput.value="";maxPriceInput.value="";amenitySelect.value="";renderListings();});
document.querySelectorAll(".category-card").forEach(button=>button.addEventListener("click",()=>{
  document.querySelectorAll(".category-card").forEach(card=>card.classList.remove("selected"));
  button.classList.add("selected");
  typeSelect.value=button.dataset.category;
  renderListings();
  document.getElementById("listings").scrollIntoView({behavior:"smooth"});
}));
grid.addEventListener("click",event=>{
  const favoriteButton=event.target.closest("[data-favorite]");
  if(favoriteButton){event.stopPropagation();const id=Number(favoriteButton.dataset.favorite);saved.has(id)?saved.delete(id):saved.add(id);renderListings();showToast(saved.has(id)?"Space saved to your favourites":"Removed from favourites");return;}
  const card=event.target.closest(".listing-card");if(card)openListing(Number(card.dataset.id));
});
grid.addEventListener("keydown",event=>{if((event.key==="Enter"||event.key===" ")&&event.target.classList.contains("listing-card")){event.preventDefault();openListing(Number(event.target.dataset.id));}});
activeFilters.addEventListener("click",event=>{const clear=event.target.closest("[data-clear]");if(!clear)return;if(clear.dataset.clear==="university")universityInput.value="";if(clear.dataset.clear==="area")areaInput.value="";if(clear.dataset.clear==="type")typeSelect.value="";if(clear.dataset.clear==="min")minPriceInput.value="";if(clear.dataset.clear==="max")maxPriceInput.value="";if(clear.dataset.clear==="amenity")amenitySelect.value="";renderListings();});
document.getElementById("clearFilters").addEventListener("click",()=>{universityInput.value="";areaInput.value="";typeSelect.value="";minPriceInput.value="";maxPriceInput.value="";amenitySelect.value="";renderListings();});
document.getElementById("showAllBtn").addEventListener("click",()=>{universityInput.value="";areaInput.value="";typeSelect.value="";minPriceInput.value="";maxPriceInput.value="";amenitySelect.value="";document.querySelectorAll(".category-card").forEach(card=>card.classList.toggle("selected",!card.dataset.category));renderListings();});
document.getElementById("dialogClose").addEventListener("click",()=>dialog.close());
dialog.addEventListener("click",event=>{if(event.target===dialog)dialog.close();});
dialogContent.addEventListener("click",event=>{const button=event.target.closest("[data-dialog-save]");if(!button)return;const id=Number(button.dataset.dialogSave);saved.has(id)?saved.delete(id):saved.add(id);button.textContent=saved.has(id)?"♥ Saved":"♡ Save space";showToast(saved.has(id)?"Space saved to your favourites":"Removed from favourites");});
document.getElementById("loginBtn").addEventListener("click",()=>showToast("Student and landlord accounts are coming soon."));
document.getElementById("menuToggle").addEventListener("click",()=>document.querySelector(".desktop-nav").classList.toggle("open"));
renderListings();