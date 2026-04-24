<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { colisApi } from '@/services/api'

const router = useRouter()
const colisList = ref([])
const loading = ref(false)
const error = ref('')
const filtreStatut = ref('TOUS')

const statutCouleurs = {
  CREE: 'bg-gray-100 text-gray-800',
  EN_TRANSIT: 'bg-blue-100 text-blue-800',
  LIVRE: 'bg-green-100 text-green-800',
  CONFIRME: 'bg-emerald-100 text-emerald-800',
}
const typeCouleurs = {
  STANDARD: 'bg-gray-50 text-gray-700',
  FRAGILE: 'bg-yellow-50 text-yellow-700',
  EXPRESS: 'bg-red-50 text-red-700',
}

const colisFiltres = computed(() => {
  if (filtreStatut.value === 'TOUS') return colisList.value
  return colisList.value.filter(c => c.statut === filtreStatut.value)
})

const chargerColis = async () => {
  loading.value = true
  error.value = ''
  try {
    colisList.value = await colisApi.lister()
  } catch (e) {
    error.value = 'Erreur de chargement : ' + (e.message || 'inconnue')
  } finally {
    loading.value = false
  }
}

const supprimerColis = async (id) => {
  if (!confirm('Supprimer ce colis ?')) return
  try {
    await colisApi.supprimer(id)
    await chargerColis()
  } catch (e) {
    alert('Erreur : ' + (e.response?.data?.detail || e.message))
  }
}

const voirDetail = (id) => router.push({ name: 'colis-detail', params: { id } })

onMounted(chargerColis)
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Liste des colis</h2>
      <RouterLink to="/colis/nouveau" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg font-medium">+ Nouveau colis</RouterLink>
    </div>

    <div class="mb-4 flex gap-2 flex-wrap">
      <button v-for="statut in ['TOUS', 'CREE', 'EN_TRANSIT', 'LIVRE', 'CONFIRME']" :key="statut"
        @click="filtreStatut = statut"
        :class="['px-3 py-1 rounded-full text-sm font-medium', filtreStatut === statut ? 'bg-indigo-600 text-white' : 'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50']">
        {{ statut }}
      </button>
    </div>

    <div v-if="loading" class="text-center py-8 text-gray-500">Chargement...</div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">{{ error }}</div>
    <div v-else-if="colisFiltres.length === 0" class="text-center py-12 bg-white rounded-lg shadow">
      <p class="text-gray-500">Aucun colis</p>
    </div>
    <div v-else class="bg-white shadow rounded-lg overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">N° suivi</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Type</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Destination</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Poids</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Statut</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="colis in colisFiltres" :key="colis.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 font-mono text-sm">{{ colis.tracking_number }}</td>
            <td class="px-6 py-4"><span :class="['px-2 py-1 text-xs rounded', typeCouleurs[colis.type_colis]]">{{ colis.type_colis }}</span></td>
            <td class="px-6 py-4 text-sm">{{ colis.adresse_destination.ville }}, {{ colis.adresse_destination.pays }}</td>
            <td class="px-6 py-4 text-sm">{{ colis.poids_kg }} kg</td>
            <td class="px-6 py-4"><span :class="['px-2 py-1 text-xs rounded-full font-medium', statutCouleurs[colis.statut]]">{{ colis.statut }}</span></td>
            <td class="px-6 py-4 text-right text-sm space-x-2">
              <button @click="voirDetail(colis.id)" class="text-indigo-600 hover:text-indigo-900">Voir</button>
              <button @click="supprimerColis(colis.id)" class="text-red-600 hover:text-red-900">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
