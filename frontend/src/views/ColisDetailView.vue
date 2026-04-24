<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { colisApi } from '@/services/api'

const props = defineProps(['id'])
const router = useRouter()

const colis = ref(null)
const historique = ref([])
const loading = ref(false)
const error = ref('')

const transitionsPossibles = computed(() => {
  if (!colis.value) return {}
  const mapping = { CREE: 'EN_TRANSIT', EN_TRANSIT: 'LIVRE', LIVRE: 'CONFIRME' }
  return mapping[colis.value.statut] ? { [colis.value.statut]: mapping[colis.value.statut] } : {}
})

const prochainStatut = computed(() => Object.values(transitionsPossibles.value)[0])

const statutCouleurs = {
  CREE: 'bg-gray-200 text-gray-800',
  EN_TRANSIT: 'bg-blue-200 text-blue-800',
  LIVRE: 'bg-green-200 text-green-800',
  CONFIRME: 'bg-emerald-200 text-emerald-800',
}

const charger = async () => {
  loading.value = true
  error.value = ''
  try {
    colis.value = await colisApi.obtenir(props.id)
    historique.value = await colisApi.historique(props.id)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erreur de chargement'
  } finally {
    loading.value = false
  }
}

const transiter = async () => {
  if (!prochainStatut.value) return
  const commentaire = prompt('Commentaire (optionnel) :') || ''
  try {
    await colisApi.transiter(props.id, prochainStatut.value, commentaire)
    await charger()
  } catch (e) {
    alert('Erreur : ' + (e.response?.data?.detail || e.message))
  }
}

const formatDate = (dateStr) => new Date(dateStr).toLocaleString('fr-FR')

onMounted(charger)
</script>

<template>
  <div class="max-w-4xl mx-auto">
    <button @click="router.push('/colis')" class="text-indigo-600 hover:underline mb-4">← Retour à la liste</button>

    <div v-if="loading" class="text-center py-8 text-gray-500">Chargement...</div>
    <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">{{ error }}</div>
    <div v-else-if="colis" class="space-y-6">
      <div class="bg-white shadow rounded-lg p-6">
        <div class="flex justify-between items-start">
          <div>
            <h2 class="text-2xl font-bold text-gray-900 font-mono">{{ colis.tracking_number }}</h2>
            <p class="text-sm text-gray-500 mt-1">Créé le {{ formatDate(colis.date_creation) }}</p>
          </div>
          <span :class="['px-4 py-2 rounded-full font-semibold', statutCouleurs[colis.statut]]">{{ colis.statut }}</span>
        </div>
        <div class="mt-4 grid grid-cols-3 gap-4 text-sm">
          <div><span class="text-gray-500">Type :</span> <span class="font-medium ml-1">{{ colis.type_colis }}</span></div>
          <div><span class="text-gray-500">Poids :</span> <span class="font-medium ml-1">{{ colis.poids_kg }} kg</span></div>
          <div><span class="text-gray-500">Dimensions :</span> <span class="font-medium ml-1">{{ colis.longueur_cm }}×{{ colis.largeur_cm }}×{{ colis.hauteur_cm }} cm</span></div>
        </div>
        <div v-if="prochainStatut" class="mt-6">
          <button @click="transiter" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-2 rounded font-medium">→ Passer à {{ prochainStatut }}</button>
        </div>
      </div>

      <div class="grid grid-cols-2 gap-6">
        <div class="bg-white shadow rounded-lg p-6">
          <h3 class="font-semibold text-gray-900 mb-2">Origine</h3>
          <p class="text-sm text-gray-700">{{ colis.adresse_origine.rue }}<br>{{ colis.adresse_origine.ville }}, {{ colis.adresse_origine.code_postal }}<br>{{ colis.adresse_origine.pays }}</p>
        </div>
        <div class="bg-white shadow rounded-lg p-6">
          <h3 class="font-semibold text-gray-900 mb-2">Destination</h3>
          <p class="text-sm text-gray-700">{{ colis.adresse_destination.rue }}<br>{{ colis.adresse_destination.ville }}, {{ colis.adresse_destination.code_postal }}<br>{{ colis.adresse_destination.pays }}</p>
        </div>
      </div>

      <div class="bg-white shadow rounded-lg p-6">
        <h3 class="font-semibold text-gray-900 mb-4">Historique des transitions</h3>
        <div v-if="historique.length === 0" class="text-sm text-gray-500">Aucune transition pour l'instant.</div>
        <ol v-else class="relative border-l-2 border-indigo-200 ml-3 space-y-4">
          <li v-for="h in historique" :key="h.id" class="ml-6">
            <span class="absolute -left-3 w-6 h-6 bg-indigo-500 rounded-full border-4 border-white"></span>
            <div class="bg-gray-50 p-3 rounded">
              <div class="flex justify-between items-center">
                <span class="font-medium text-gray-900">{{ h.statut_precedent }} → {{ h.statut_nouveau }}</span>
                <span class="text-xs text-gray-500">{{ formatDate(h.date_transition) }}</span>
              </div>
              <p v-if="h.commentaire" class="text-sm text-gray-600 mt-1 italic">"{{ h.commentaire }}"</p>
            </div>
          </li>
        </ol>
      </div>
    </div>
  </div>
</template>
