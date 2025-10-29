<template>
  <div class="p-4">
    <h2 class="text-2xl font-bold mb-4">剧情弧光 / 伏笔管理</h2>
    <div class="mb-4">
      <button @click="isCreating = true" class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
        添加新弧光
      </button>
    </div>

    <!-- Create/Edit Form -->
    <div v-if="isCreating || editingArc" class="mb-4 p-4 bg-gray-50 rounded-lg">
      <h3 class="text-lg font-semibold mb-2">{{ editingArc ? '编辑弧光' : '创建新弧光' }}</h3>
      <textarea v-model="form.description" class="w-full p-2 border rounded" placeholder="描述剧情弧光..."></textarea>
      <div class="mt-2">
        <label class="mr-2">状态:</label>
        <select v-model="form.status" class="p-2 border rounded">
          <option value="unresolved">未解决</option>
          <option value="resolved">已解决</option>
        </select>
      </div>
      <div class="mt-4">
        <button @click="saveArc" class="px-4 py-2 bg-green-600 text-white rounded-lg mr-2">保存</button>
        <button @click="cancelEdit" class="px-4 py-2 bg-gray-300 rounded-lg">取消</button>
      </div>
    </div>

    <!-- Arcs List -->
    <div v-if="isLoading" class="text-center">加载中...</div>
    <div v-else-if="error" class="text-red-500">{{ error }}</div>
    <div v-else>
      <div v-for="arc in arcs" :key="arc.id" class="p-4 mb-2 border rounded-lg flex justify-between items-center">
        <div>
          <p>{{ arc.description }}</p>
          <span :class="['text-sm', arc.status === 'resolved' ? 'text-green-600' : 'text-yellow-600']">{{ arc.status }}</span>
        </div>
        <div>
          <button @click="startEdit(arc)" class="px-3 py-1 bg-blue-500 text-white rounded-lg mr-2">编辑</button>
          <button @click="deleteArc(arc.id)" class="px-3 py-1 bg-red-500 text-white rounded-lg">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { PlotArcAPI, type PlotArc } from '@/api/novel';

const route = useRoute();
const projectId = route.params.id as string;

const arcs = ref<PlotArc[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);

const isCreating = ref(false);
const editingArc = ref<PlotArc | null>(null);
const form = ref({
  description: '',
  status: 'unresolved'
});

const loadArcs = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    arcs.value = await PlotArcAPI.getPlotArcs(projectId);
  } catch (e) {
    error.value = e instanceof Error ? e.message : '加载剧情弧光失败';
  } finally {
    isLoading.value = false;
  }
};

const startEdit = (arc: PlotArc) => {
  editingArc.value = arc;
  form.value.description = arc.description;
  form.value.status = arc.status;
  isCreating.value = false;
};

const cancelEdit = () => {
  isCreating.value = false;
  editingArc.value = null;
  form.value.description = '';
  form.value.status = 'unresolved';
};

const saveArc = async () => {
  if (editingArc.value) {
    // Update
    await PlotArcAPI.updatePlotArc(projectId, editingArc.value.id, form.value);
  } else {
    // Create
    await PlotArcAPI.createPlotArc(projectId, form.value);
  }
  cancelEdit();
  loadArcs();
};

const deleteArc = async (arcId: number) => {
  if (confirm('确定要删除这个剧情弧光吗？')) {
    await PlotArcAPI.deletePlotArc(projectId, arcId);
    loadArcs();
  }
};

onMounted(loadArcs);
</script>