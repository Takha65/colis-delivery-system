<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { colisApi } from '@/services/api'

const router = useRouter()
const form = ref({
  poids_kg: 2.5,
  longueur_cm: 30,
  largeur_cm: 20,
  hauteur_cm: 10,
  rue_origine: '',
  ville_origine: 'Sherbrooke',
  code_postal_origine: '',
  rue_destination: '',
  ville_destination: 'Montreal',
  code_postal_destination: '',
  type_colis: 'STANDARD',
})
const loading = ref(false)
const error = ref('')

const submit = async () => {
  loading.value = true
  error.value = ''
  try {
    const colis = await colisApi.creer(form.value)
    router.push({ name: 'colis-detail', params: { id: colis.id } })
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erreur de creation'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-3xl mx-auto">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Créer un colis</h2>
    <form @submit.prevent="submit" class="bg-white shadow rounded-lg p-6 space-y-6">
      <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">{{ error }}</div>

      <div>
        <h3 class="text-lg font-semibold text-gray-900 mb-3">Caractéristiques</h3>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Type</label>
            <select v-model="form.type_colis" class="mt-1 block w-full rounded border-gray-300 shadow-sm">
              <option value="STANDARD">Standard</option>
              <option value="FRAGILE">Fragile (≤ 20 kg)</option>
              <option value="EXPRESS">Express (≤ 10 kg)</option>
            </select>
          </div>
          <div><label class="block text-sm font-medium text-gray-700">Poids (kg)</label><input type="number" step="0.1" v-model.number="form.poids_kg" required class="mt-1 block w-full rounded border-gray-300 shadow-sm" /></div>
          <div><label class="block text-sm font-medium text-gray-700">Longueur (cm)</label><input type="number" v-model.number="form.longueur_cm" required class="mt-1 block w-full rounded border-gray-300 shadow-sm" /></div>
          <div><label class="block text-sm font-medium text-gray-700">Largeur (cm)</label><input type="number" v-model.number="form.largeur_cm" required class="mt-1 block w-full rounded border-gray-300 shadow-sm" /></div>
          <div><label class="block text-sm font-medium text-gray-700">Hauteur (cm)</label><input type="number" v-model.number="form.hauteur_cm" required class="mt-1 block w-full rounded border-gray-300 shadow-sm" /></div>
        </div>
      </div>

      <div>
        <h3 class="text-lg font-semibold text-gray-900 mb-3">Adresse d'origine</h3>
        <div class="grid grid-cols-2 gap-4">
          <div class="col-span-2"><label class="block text-sm font-medium text-gray-700">Rue</label><input type="text" v-model="form.rue_origine" required placeholder="ex: 2500 Boul Universite" class="mt-1 block w-full rounded border-gray-300 shadow-sm" /></div>
          <div><label class="block text-sm font-medium text-gray-700">Ville</label><input type="text" v-model="form.ville_origine" required class="mt-1 block w-full rounded border-gray-300 shadow-sm" /></div>
          <div><label class="block text-sm font-medium text-gray-700">Code postal</label><input type="text" v-model="form.code_postal_origine" required placeholder="J1K 2R1" class="mt-1 block w-full rounded border-gray-300 shadow-sm" /></div>
        </div>
      </div>

      <div>
        <h3 class="text-lg font-semibold text-gray-900 mb-3">Adresse de destination</h3>
        <div class="grid grid-cols-2 gap-4">
          <div class="col-span-2"><label class="block text-sm font-medium text-gray-700">Rue</label><input type="text" v-model="form.rue_destination" required class="mt-1 block w-full rounded border-gray-300 shadow-sm" /></div>
          <div><label class="block text-sm font-medium text-gray-700">Ville</label><input type="text" v-model="form.ville_destination" required class="mt-1 block w-full rounded border-gray-300 shadow-sm" /></div>
          <div><label class="block text-sm font-medium text-gray-700">Code postal</label><input type="text" v-model="form.code_postal_destination" required class="mt-1 block w-full rounded border-gray-300 shadow-sm" /></div>
        </div>
        <p class="mt-2 text-sm text-gray-500">📍 Les adresses seront géocodées automatiquement via Nominatim</p>
      </div>

      <div class="flex justify-end gap-3">
        <button type="button" @click="router.push('/colis')" class="px-4 py-2 border border-gray-300 rounded text-gray-700 hover:bg-gray-50">Annuler</button>
        <button type="submit" :disabled="loading" class="px-6 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 disabled:opacity-50">{{ loading ? 'Création...' : 'Créer' }}</button>
      </div>
    </form>
  </div>
</template>
