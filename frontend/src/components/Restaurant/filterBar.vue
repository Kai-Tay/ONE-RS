<script setup>
import { TagsInput, TagsInputItem, TagsInputItemDelete, TagsInputItemText } from '@/components/ui/tags'
import { ref } from 'vue'
</script>

<template>
  
  <TagsInput v-model="modelValue">
    <TagsInputItem v-for="item in modelValue" :key="item" :value="item">
      <TagsInputItemText />
      <TagsInputItemDelete />
    </TagsInputItem>
  </TagsInput>
</template>

<script>
export default {
  props: {
    searchValue: ""
  },
  data() {
    return {
      searchResults: []
    }
  }
}

</script>