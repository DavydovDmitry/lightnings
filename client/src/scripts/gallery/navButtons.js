export const navButtons = {
  left: {
    element: document.querySelector('.gallery-button:first-child'),

    activate() {
      this.element.classList.add('active');
    },
    deactivate() {
      this.element.classList.remove('active');
    },
  },

  right: {
    element: document.querySelector('.gallery-button:last-child'),

    activate() {
      this.element.classList.add('active');
    },
    deactivate() {
      this.element.classList.remove('active');
    },
  }
}
