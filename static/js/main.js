document.addEventListener("DOMContentLoaded", () => {
  // Search functionality
  const searchInput = document.getElementById("searchInput")
  const searchResults = document.getElementById("searchResults")
  const searchResultTemplate = document.getElementById("search-result-template")

  if (searchInput && searchResults && searchResultTemplate) {
    let searchTimeout

    // Debounce function to limit API calls
    const debounce = (func, delay) => {
      return function () {

        const args = arguments
        clearTimeout(searchTimeout)
        searchTimeout = setTimeout(() => func.apply(this, args), delay)
      }
    }

    // Optimized search handler
    const handleSearch = debounce(function () {
      const query = this.value.trim()

      if (query.length < 2) {
        searchResults.style.display = "none"
        return
      }

      fetch(`/ajax/search/?q=${encodeURIComponent(query)}`)
          .then((response) => response.json())
          .then((data) => {
            searchResults.innerHTML = ""

            if (data.results.length > 0) {
              // Use document fragment for better performance
              const fragment = document.createDocumentFragment()

              data.results.forEach((video, index) => {
                const resultItem = searchResultTemplate.content.cloneNode(true)
                const link = resultItem.querySelector("a")
                const img = resultItem.querySelector("img")
                const title = resultItem.querySelector(".search-result-title")
                const meta = resultItem.querySelector(".search-result-meta")

                link.href = video.url
                img.src = video.poster || "/static/img/placeholder-poster.jpg"
                img.alt = video.title
                title.textContent = video.title
                meta.textContent = `${video.year} • ${video.content_type}`

                // Add animation with delay based on index
                link.classList.add("animate__animated", "animate__fadeInDown")
                link.style.animationDelay = `${index * 0.05}s`

                fragment.appendChild(resultItem)
              })

              // Add "See all results" link
              const seeAllLink = document.createElement("a")
              seeAllLink.href = `/search/?q=${encodeURIComponent(query)}`
              seeAllLink.className = "search-result-item see-all animate__animated animate__fadeInUp"
              seeAllLink.textContent = `Barcha natijalarni ko'rish: "${query}"`
              fragment.appendChild(seeAllLink)

              // Append all elements at once for better performance
              searchResults.appendChild(fragment)
              searchResults.style.display = "block"
            } else {
              searchResults.style.display = "none"
            }
          })
          .catch((error) => {
            console.error("Search error:", error)
          })
    }, 300)

    searchInput.addEventListener("input", handleSearch)

    // Hide search results when clicking outside
    document.addEventListener("click", (event) => {
      if (!searchInput.contains(event.target) && !searchResults.contains(event.target)) {
        searchResults.style.display = "none"
      }
    })

    // Show results when input is focused if there's a query
    searchInput.addEventListener("focus", function () {
      if (this.value.trim().length >= 2) {
        handleSearch.call(this)
      }
    })
  }

  // Video slider functionality
  const sliders = document.querySelectorAll(".video-slider")

  sliders.forEach((slider) => {
    const prevArrow = slider.querySelector(".prev-arrow")
    const nextArrow = slider.querySelector(".next-arrow")
    const videoGrid = slider.querySelector(".video-grid")

    if (prevArrow && nextArrow && videoGrid) {
      const scrollAmount = 3 * (videoGrid.querySelector(".video-card")?.offsetWidth || 200)

      prevArrow.addEventListener("click", () => {
        videoGrid.scrollBy({
          left: -scrollAmount,
          behavior: "smooth",
        })
      })

      nextArrow.addEventListener("click", () => {
        videoGrid.scrollBy({
          left: scrollAmount,
          behavior: "smooth",
        })
      })
    }
  })

  // Video player controls
  const videoPlayer = document.getElementById("videoPlayer")

  if (videoPlayer && videoPlayer.tagName === "VIDEO") {
    const playButton = document.querySelector(".play-button")
    const muteButton = document.querySelector(".mute-button")
    const fullscreenButton = document.querySelector(".fullscreen-button")
    const progressBar = document.querySelector(".progress-bar")
    const progressFilled = document.querySelector(".progress-filled")

    // Play/Pause
    playButton?.addEventListener("click", () => {
      if (videoPlayer.paused) {
        videoPlayer.play()
        playButton.innerHTML = '<i class="fas fa-pause"></i>'
      } else {
        videoPlayer.pause()
        playButton.innerHTML = '<i class="fas fa-play"></i>'
      }
    })

    // Mute/Unmute
    muteButton?.addEventListener("click", () => {
      videoPlayer.muted = !videoPlayer.muted
      muteButton.innerHTML = videoPlayer.muted
          ? '<i class="fas fa-volume-mute"></i>'
          : '<i class="fas fa-volume-up"></i>'
    })

    // Fullscreen
    fullscreenButton?.addEventListener("click", () => {
      if (videoPlayer.requestFullscreen) {
        videoPlayer.requestFullscreen()
      } else if (videoPlayer.webkitRequestFullscreen) {
        videoPlayer.webkitRequestFullscreen()
      } else if (videoPlayer.msRequestFullscreen) {
        videoPlayer.msRequestFullscreen()
      }
    })

    // Update progress bar
    videoPlayer.addEventListener("timeupdate", () => {
      if (progressFilled) {
        const percent = (videoPlayer.currentTime / videoPlayer.duration) * 100
        progressFilled.style.width = `${percent}%`
      }
    })

    // Click on progress bar
    progressBar?.addEventListener("click", (e) => {
      const progressTime = (e.offsetX / progressBar.offsetWidth) * videoPlayer.duration
      videoPlayer.currentTime = progressTime
    })
  }

  // Add animation to elements when they come into view
  const animateOnScroll = () => {
    const elements = document.querySelectorAll(".section, .video-card, .comment, .auth-box")

    elements.forEach((element) => {
      const elementPosition = element.getBoundingClientRect().top
      const screenPosition = window.innerHeight

      if (elementPosition < screenPosition) {
        if (!element.classList.contains("animate__animated")) {
          element.classList.add("animate__animated", "animate__fadeIn")
        }
      }
    })
  }

  // Run on scroll
  window.addEventListener("scroll", animateOnScroll)

  // Run once on page load
  animateOnScroll()

  // Helper function to get CSRF token
  function getCookie(name) {
    let cookieValue = null
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";")
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim()
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
          break
        }
      }
    }
    return cookieValue
  }
})

// Add staggered animation for lists
document.addEventListener("DOMContentLoaded", () => {
  const staggerContainers = document.querySelectorAll(".video-grid, .comments-list")

  staggerContainers.forEach((container) => {
    const items = container.children

    for (let i = 0; i < items.length; i++) {
      items[i].style.animationDelay = `${i * 0.05}s`
    }
  })
})

// Add hover animations for interactive elements
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".btn, .auth-button, .submit-button")

  buttons.forEach((button) => {
    button.addEventListener("mouseenter", function () {
      this.classList.add("animate__animated", "animate__pulse")
    })

    button.addEventListener("mouseleave", function () {
      this.classList.remove("animate__animated", "animate__pulse")
    })
  })
})
