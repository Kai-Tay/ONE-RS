export default {
  // ... existing code ...
  created() {
    // Add listener for auth state changes
    this.$root.$on('auth-state-changed', () => {
      this.checkAuthStatus(); // Or whatever method you use to update the UI
    });
  },
  beforeDestroy() {
    // Clean up the event listener
    this.$root.$off('auth-state-changed');
  }
  // ... rest of the component
} 