<template>
  <div class="test-component">
    <h1>{{ title }}</h1>
    <p>Count: {{ count }}</p>
    <button @click="increment">Increment</button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'

interface Props {
  title: string
  initialCount?: number
}

const props = withDefaults(defineProps<Props>(), {
  initialCount: 0
})

const count = ref(props.initialCount)

const doubleCount = computed(() => count.value * 2)

function increment() {
  count.value++
}

// Method without breadcrumb documentation
function undocumentedMethod() {
  count.value = 0
}

onMounted(() => {
  console.log('Component mounted')
})

watch(count, (newValue, oldValue) => {
  console.log(`Count changed from ${oldValue} to ${newValue}`)
})

async function asyncMethod(data: string): Promise<string> {
  return new Promise(resolve => {
    setTimeout(() => resolve(data.toUpperCase()), 100)
  })
}

const emit = defineEmits<{
  update: [value: number]
  click: [event: MouseEvent]
}>()

defineExpose({
  increment,
  reset: () => count.value = 0
})
</script>

<script lang="ts">
export default {
  name: 'TestVueComponent',
  
  data() {
    return {
      message: 'Hello Vue'
    }
  },
  
  computed: {
    upperMessage() {
      return this.message.toUpperCase()
    }
  },
  
  methods: {
    updateMessage(newMessage: string) {
      this.message = newMessage
    }
  },
  
  mounted() {
    console.log('Options API component mounted')
  }
}
</script>

<style scoped>
.test-component {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.test-component h1 {
  color: #333;
  margin-bottom: 0.5rem;
}

.test-component button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}

.test-component button:hover {
  background-color: #0056b3;
}
</style>