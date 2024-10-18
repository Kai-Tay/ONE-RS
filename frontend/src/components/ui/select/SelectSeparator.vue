<script setup>
import { cn } from '@/lib/utils';
import { SelectSeparator } from 'radix-vue';
import { computed } from 'vue';

const props = defineProps({
  asChild: { type: Boolean, required: false },
  as: { type: null, required: false },
  class: { type: null, required: false },
});

const delegatedProps = computed(() => {
  const { class: _, ...delegated } = props;

  return delegated;
});
</script>

<template>
  <SelectSeparator
    v-bind="delegatedProps"
    :class="cn('tw--mx-1 tw-my-1 tw-h-px tw-bg-muted', props.class)"
  />
</template>
