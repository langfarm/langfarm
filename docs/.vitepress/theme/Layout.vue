<script lang="ts" setup>
import { nextTick, onMounted, watch } from 'vue';

import mediumZoom from 'medium-zoom';
import { useRoute } from 'vitepress';
import DefaultTheme from 'vitepress/theme';
import mermaid from 'mermaid';

const { Layout } = DefaultTheme;
const route = useRoute();

const on_page_change = () => {
  mediumZoom('.VPDoc img', { background: 'var(--vp-c-bg)' });
  mermaid.run()
};

watch(
    () => route.path,
    () => nextTick(() => on_page_change()),
);

onMounted(() => {
  mermaid.initialize({ startOnLoad: false });
  on_page_change();
});

</script>

<template>
  <Layout />
</template>

<style>
.medium-zoom-overlay,
.medium-zoom-image--opened {
  z-index: 2147483647;
}
</style>
