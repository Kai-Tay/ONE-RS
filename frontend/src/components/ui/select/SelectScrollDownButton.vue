<script setup>
import { cn } from '@/lib/utils';
import { ChevronDown } from 'lucide-vue-next';
import { SelectScrollDownButton, useForwardProps } from 'radix-vue';
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

const forwardedProps = useForwardProps(delegatedProps);
</script>

<template>
  <SelectScrollDownButton
    v-bind="forwardedProps"
    :class="
      cn('tw-flex tw-cursor-default tw-items-center tw-justify-center tw-py-1', props.class)
    "
  >
    <slot>
      <ChevronDown class="tw-h-4 tw-w-4" />
    </slot>
  </SelectScrollDownButton>
</template>
