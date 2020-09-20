export let mediaContainer = {
  element: document.querySelector('#multimedia-container'),
  activeIndex: 0,

  showFirst() {
    this.activeIndex = 0;
    showActive();
  },

  showNext() {
    if (!this.isLastActive()) {
      hideActive();
      this.activeIndex++;
      showActive();
    }
  },

  showPrev() {
    if (!this.isFirstActive()) {
      hideActive();
      this.activeIndex--;
      showActive();
    }
  },

  isFirstActive() {
    return this.activeIndex === 0;
  },

  isLastActive() {
    return this.activeIndex === mediaContainer.element.querySelectorAll('.multimedia').length - 1
  },

  removeAllMedia() {
    this.element.querySelectorAll('.multimedia').forEach((media) => {
        media.remove();
    });
  }
}

function showActive() {
  let multimedia = mediaContainer.element.querySelectorAll('.multimedia');
  multimedia[mediaContainer.activeIndex].style.display = 'flex';
}

function hideActive() {
  let multimedia = mediaContainer.element.querySelectorAll('.multimedia');
  multimedia[mediaContainer.activeIndex].style.display = 'none';
}
