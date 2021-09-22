const settingsNavItem = document.getElementsByClassName("settings-nav-item")

for (var i=0;i<settingsNavItem.length;i++){
    settingsNavItem[i].addEventListener("click",function(){
        tab = this.dataset.tab;
        const url = new URL(window.location.href);
        url.searchParams.set('tab', tab);
        window.location = `${url}`
    })
}

let url = new URL(window.location)
let parms = new URLSearchParams(url.search)
let tab = parms.get("tab")

if(tab){
    const tabContainer = document.getElementById(tab)
    const tabButton = document.getElementsByClassName(tab)[0]
    tabContainer.classList.remove("fade")
    tabContainer.classList.add("active")
    tabButton.classList.add("active")
    console.log(tabContainer)
}



