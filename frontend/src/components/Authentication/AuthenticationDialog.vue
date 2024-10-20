<script setup>
import { Dialog, DialogHeader, DialogContent, DialogTitle, DialogDescription, DialogClose, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
</script>

<!-- HTML STUFF -->
<template>
  <!-- Sign In Success Dialog -->
  <Dialog :open="showDialog" v-if="success">
    <DialogContent>
      <DialogHeader>
        <DialogTitle class="tw-text-xl">{{ status }}</DialogTitle>
      </DialogHeader>
      <DialogDescription>
          {{ description }}
        </DialogDescription>
    </DialogContent>
  </Dialog>

  <!-- Sign In UnSuccess Dialog -->
  <Dialog :open="showDialog" v-else>
    <DialogContent>
      <DialogHeader>
        <DialogTitle class="tw-text-xl">{{ status }}</DialogTitle>
      </DialogHeader>
      <DialogDescription>
          {{description}}
        </DialogDescription>
        <DialogFooter class="sm:justify-start">
        <DialogClose as-child>
          <Button type="button" variant="secondary" @click="closeDialog">
            Close
          </Button>
        </DialogClose>
      </DialogFooter>
    </DialogContent>
  </Dialog>
  

</template>

<!-- VUE STUFF -->
<script>
export default {
  name: 'AuthenticationDialog',
  props: {
    showDialog: {
      type: Boolean,
      default: false,
    },
    status: {
      type: String,
      default: '',
    },
    description: {
      type: String,
      default: '',
    },
    success: {
      type: Boolean,
      default: true,
    },
},
methods: {
  closeDialog() {
    this.$emit('update:showDialog', false); // Emit an event to close the dialog
  }
}
}
</script>

<!-- CSS STUFF -->
<style>


/* Removed x from dialog */
.lucide{
  display: none;
  outline: none;
}


/* If you want to ensure no focus styles apply */
.tw-absolute.tw-right-4.tw-top-4.tw-rounded-sm {
    --tw-ring-color: transparent; /* Disable ring color */
}

.tw-absolute.tw-right-4.tw-top-4.tw-rounded-sm:focus {
    box-shadow: none; /* Remove any box shadow on focus */
}
</style>