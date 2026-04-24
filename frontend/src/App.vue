<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between h-16 items-center">
          <div class="flex items-center space-x-8">
            <h1 class="text-xl font-bold text-gray-900">📦 Colis Delivery</h1>
            <div class="flex space-x-4">
              <RouterLink to="/colis" class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded" active-class="text-indigo-600 font-semibold">Colis</RouterLink>
              <RouterLink to="/colis/nouveau" class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded" active-class="text-indigo-600 font-semibold">Nouveau colis</RouterLink>
              <RouterLink to="/route-planner" class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded" active-class="text-indigo-600 font-semibold">Planificateur</RouterLink>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <main class="max-w-7xl mx-auto px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>
