<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-4">写作原则 / 写作宪法管理</h2>
    <div class="mb-4">
      <button @click="isCreating = true" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
        添加新原则
      </button>
    </div>

    <!-- Create/Edit Form -->
    <div v-if="isCreating || editingPrinciple" class="mb-4 p-4 bg-gray-50 rounded-lg">
      <h3 class="text-lg font-semibold mb-2">{{ editingPrinciple ? '编辑原则' : '创建新原则' }}</h3>
      <div class="space-y-2">
        <input v-model="form.risk_topic" class="w-full p-2 border rounded" placeholder="风险主题 (例如：节奏失控)">
        <textarea v-model="form.core_problem" class="w-full p-2 border rounded" placeholder="核心问题..."></textarea>
        <textarea v-model="form.guiding_principle" class="w-full p-2 border rounded" placeholder="指导原则..."></textarea>
        <label class="flex items-center">
          <input type="checkbox" v-model="form.is_enabled" class="mr-2">
          启用
        </label>
      </div>
      <div class="mt-4">
        <button @click="savePrinciple" class="px-4 py-2 bg-green-600 text-white rounded-lg mr-2">保存</button>
        <button @click="cancelEdit" class="px-4 py-2 bg-gray-300 rounded-lg">取消</button>
      </div>
    </div>

    <!-- Principles List -->
    <div v-if="isLoading" class="text-center">加载中...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else>
      <div v-for="principle in principles" :key="principle.id" class="p-4 mb-2 border rounded-lg">
        <div class="flex justify-between items-center">
          <h4 class="font-bold">{{ principle.risk_topic }}</h4>
          <div>
            <button @click="startEdit(principle)" class="px-3 py-1 bg-blue-500 text-white rounded-lg mr-2">编辑</button>
            <button @click="deletePrinciple(principle.id)" class="px-3 py-1 bg-red-500 text-white rounded-lg">删除</button>
          </div>
        </div>
        <p class="text-sm text-gray-600 mt-1">{{ principle.core_problem }}</p>
        <p class="mt-2"><strong>指导原则:</strong> {{ principle.guiding_principle }}</p>
        <span :class="['text-sm', principle.is_enabled ? 'text-green-600' : 'text-gray-500']">{{ principle.is_enabled ? '已启用' : '已禁用' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { WritingPrincipleAPI, type WritingPrinciple } from '@/api/novel';

const route = useRoute();
const projectId = route.params.id as string;

const principles = ref<WritingPrinciple[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);

const isCreating = ref(false);
const editingPrinciple = ref<WritingPrinciple | null>(null);
const form = ref({
  risk_topic: '',
  core_problem: '',
  guiding_principle: '',
  is_enabled: true
});

const loadPrinciples = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    principles.value = await WritingPrincipleAPI.getWritingPrinciples(projectId);
  } catch (e) {
    error.value = e instanceof Error ? e.message : '加载写作原则失败';
  } finally {
    isLoading.value = false;
  }
};

const startEdit = (principle: WritingPrinciple) => {
  editingPrinciple.value = principle;
  form.value = { ...principle };
  isCreating.value = false;
};

const cancelEdit = () => {
  isCreating.value = false;
  editingPrinciple.value = null;
  form.value = {
    risk_topic: '',
    core_problem: '',
    guiding_principle: '',
    is_enabled: true
  };
};

const savePrinciple = async () => {
  if (editingPrinciple.value) {
    // Update
    await WritingPrincipleAPI.updateWritingPrinciple(projectId, editingPrinciple.value.id, form.value);
  } else {
    // Create
    await WritingPrincipleAPI.createWritingPrinciple(projectId, form.value);
  }
  cancelEdit();
  loadPrinciples();
};

const deletePrinciple = async (principleId: number) => {
  if (confirm('确定要删除这个写作原则吗？')) {
    await WritingPrincipleAPI.deleteWritingPrinciple(projectId, principleId);
    loadPrinciples();
  }
};

onMounted(loadPrinciples);
</script>