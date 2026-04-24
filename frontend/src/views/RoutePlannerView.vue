<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { livreursApi, routageApi } from '@/services/api'

const livreurs = ref([])
const noeuds = ref([])
const strategies = ref([])

const livreurSelectionne = ref('')
const noeudsAVisiter = ref([])
const noeudDepart = ref('')
const strategieChoisie = ref('')

const poidsDistance = ref(50)
const poidsTemps = ref(30)
const poidsCharge = ref(20)

const nouveauLivreur = ref({ nom: '', capacite_max_kg: 50, position_depart_id: '' })
const showNouveauLivreur = ref(false)

const routeCalculee = ref(null)
const comparaisons = ref([])
const loading = ref(false)
const error = ref('')

const poidsValides = computed(() => Math.abs(poidsDistance.value + poidsTemps.value + poidsCharge.value - 100) < 1)
const peutCalculer = computed(() => livreurSelectionne.value && noeudDepart.value && noeudsAVisiter.value.length > 0 && poidsValides.value)

const charger = async () => {
  try {
    const [l, g, s] = await Promise.all([livreursApi.lister(), routageApi.graphe(), routageApi.strategies()])
    livreurs.value = l
    noeuds.value = g.noeuds
    strategies.value = s
  } catch (e) {
    error.value = 'Erreur : ' + e.message
  }
}

const toggleNoeudAVisiter = (nid) => {
  const idx = noeudsAVisiter.value.indexOf(nid)
  if (idx >= 0) noeudsAVisiter.value.splice(idx, 1)
  else noeudsAVisiter.value.push(nid)
}

const calculer = async () => {
  error.value = ''
  loading.value = true
  routeCalculee.value = null
  comparaisons.value = []
  try {
    routeCalculee.value = await routageApi.calculer({
      livreur_id: livreurSelectionne.value,
      noeud_depart: noeudDepart.value,
      noeuds_a_visiter: noeudsAVisiter.value,
      poids_distance: poidsDistance.value / 100,
      poids_temps: poidsTemps.value / 100,
      poids_charge: poidsCharge.value / 100,
      strategie: strategieChoisie.value || undefined,
    })
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erreur de calcul'
  } finally {
    loading.value = false
  }
}

const comparerStrategies = async () => {
  error.value = ''
  loading.value = true
  routeCalculee.value = null
  comparaisons.value = []
  try {
    const results = await Promise.all(
      strategies.value.map(s =>
        routageApi.calculer({
          livreur_id: livreurSelectionne.value,
          noeud_depart: noeudDepart.value,
          noeuds_a_visiter: noeudsAVisiter.value,
          poids_distance: poidsDistance.value / 100,
          poids_temps: poidsTemps.value / 100,
          poids_charge: poidsCharge.value / 100,
          strategie: s.nom,
        })
      )
    )
    comparaisons.value = results
  } catch (e) {
    error.value = e.response?.data?.detail || 'Erreur de comparaison'
  } finally {
    loading.value = false
  }
}

const creerLivreur = async () => {
  try {
    const l = await livreursApi.creer(nouveauLivreur.value)
    livreurs.value.push(l)
    livreurSelectionne.value = l.id
    showNouveauLivreur.value = false
  } catch (e) {
    alert('Erreur : ' + (e.response?.data?.detail || e.message))
  }
}

watch(livreurSelectionne, (id) => {
  const l = livreurs.value.find(x => x.id === id)
  if (l) noeudDepart.value = l.position_depart_id
})

onMounted(charger)
</script>

<template>
  <div class="space-y-6">
    <h2 class="text-2xl font-bold text-gray-900">Planificateur de route</h2>
    <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">{{ error }}</div>

    <div class="bg-white shadow rounded-lg p-6 space-y-6">
      <div>
        <div class="flex justify-between items-center mb-2">
          <label class="block text-sm font-medium text-gray-700">Livreur</label>
          <button @click="showNouveauLivreur = !showNouveauLivreur" class="text-sm text-indigo-600 hover:underline">+ Créer un livreur</button>
        </div>
        <select v-model="livreurSelectionne" class="block w-full rounded border-gray-300 shadow-sm">
          <option value="">-- Choisir --</option>
          <option v-for="l in livreurs" :key="l.id" :value="l.id">{{ l.nom }} (capacité {{ l.capacite_max_kg }}kg, départ {{ l.position_depart_id }})</option>
        </select>
        <div v-if="showNouveauLivreur" class="mt-3 p-3 bg-gray-50 rounded border">
          <div class="grid grid-cols-3 gap-2">
            <input v-model="nouveauLivreur.nom" placeholder="Nom" class="rounded border-gray-300" />
            <input type="number" v-model.number="nouveauLivreur.capacite_max_kg" placeholder="Capacité kg" class="rounded border-gray-300" />
            <select v-model="nouveauLivreur.position_depart_id" class="rounded border-gray-300">
              <option value="">-- Départ --</option>
              <option v-for="n in noeuds" :key="n.id" :value="n.id">{{ n.nom }}</option>
            </select>
          </div>
          <button @click="creerLivreur" class="mt-2 bg-indigo-600 text-white px-3 py-1 rounded text-sm">Créer</button>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Point de départ</label>
        <select v-model="noeudDepart" class="block w-full rounded border-gray-300 shadow-sm">
          <option value="">-- Choisir --</option>
          <option v-for="n in noeuds" :key="n.id" :value="n.id">{{ n.nom }}</option>
        </select>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Points à visiter ({{ noeudsAVisiter.length }} sélectionnés)</label>
        <div class="grid grid-cols-4 gap-2">
          <button v-for="n in noeuds" :key="n.id" @click="toggleNoeudAVisiter(n.id)" :disabled="n.id === noeudDepart"
            :class="['px-3 py-2 rounded border text-sm', noeudsAVisiter.includes(n.id) ? 'bg-indigo-600 text-white border-indigo-600' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50', n.id === noeudDepart ? 'opacity-30 cursor-not-allowed' : '']">
            {{ n.nom }}
          </button>
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-3">Critères (total doit être 100%, actuellement {{ poidsDistance + poidsTemps + poidsCharge }}%)</label>
        <div class="space-y-3">
          <div>
            <div class="flex justify-between text-sm"><span>🛣️ Distance</span><span class="font-medium">{{ poidsDistance }}%</span></div>
            <input type="range" min="0" max="100" v-model.number="poidsDistance" class="w-full" />
          </div>
          <div>
            <div class="flex justify-between text-sm"><span>⏱️ Temps</span><span class="font-medium">{{ poidsTemps }}%</span></div>
            <input type="range" min="0" max="100" v-model.number="poidsTemps" class="w-full" />
          </div>
          <div>
            <div class="flex justify-between text-sm"><span>🚦 Charge (anti-trafic)</span><span class="font-medium">{{ poidsCharge }}%</span></div>
            <input type="range" min="0" max="100" v-model.number="poidsCharge" class="w-full" />
          </div>
        </div>
        <p v-if="!poidsValides" class="text-sm text-red-600 mt-2">⚠️ La somme doit être exactement 100%</p>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Stratégie</label>
        <select v-model="strategieChoisie" class="block w-full rounded border-gray-300 shadow-sm">
          <option value="">Automatique (selon nb de colis)</option>
          <option v-for="s in strategies" :key="s.nom" :value="s.nom">{{ s.nom }} — {{ s.description }}</option>
        </select>
      </div>

      <div class="flex gap-3">
        <button @click="calculer" :disabled="!peutCalculer || loading" class="flex-1 bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 disabled:opacity-50">{{ loading ? 'Calcul...' : '🎯 Calculer la route' }}</button>
        <button @click="comparerStrategies" :disabled="!peutCalculer || loading" class="flex-1 bg-purple-600 text-white py-2 rounded hover:bg-purple-700 disabled:opacity-50">📊 Comparer les 3 stratégies</button>
      </div>
    </div>

    <div v-if="routeCalculee" class="bg-white shadow rounded-lg p-6">
      <h3 class="text-lg font-semibold mb-3">Route calculée — <span class="text-indigo-600">{{ routeCalculee.strategie_utilisee }}</span></h3>
      <div class="grid grid-cols-4 gap-4 mb-4 text-center">
        <div class="bg-gray-50 rounded p-3"><div class="text-2xl font-bold text-gray-900">{{ routeCalculee.distance_totale_km.toFixed(1) }}</div><div class="text-xs text-gray-500">km</div></div>
        <div class="bg-gray-50 rounded p-3"><div class="text-2xl font-bold text-gray-900">{{ Math.round(routeCalculee.temps_total_minutes) }}</div><div class="text-xs text-gray-500">minutes</div></div>
        <div class="bg-gray-50 rounded p-3"><div class="text-2xl font-bold text-gray-900">{{ (routeCalculee.charge_moyenne * 100).toFixed(0) }}%</div><div class="text-xs text-gray-500">charge moy.</div></div>
        <div class="bg-gray-50 rounded p-3"><div class="text-2xl font-bold text-gray-900">{{ routeCalculee.nombre_arrets }}</div><div class="text-xs text-gray-500">arrêts</div></div>
      </div>
      <ol class="space-y-2">
        <li v-for="e in routeCalculee.etapes" :key="e.ordre" class="flex items-center gap-3 bg-gray-50 rounded p-2">
          <span class="bg-indigo-600 text-white rounded-full w-7 h-7 flex items-center justify-center font-bold text-sm">{{ e.ordre }}</span>
          <span class="font-medium">{{ e.nom_lieu }}</span>
          <span v-if="e.ordre > 0" class="text-sm text-gray-500 ml-auto">{{ e.distance_depuis_precedent_km.toFixed(1) }} km · {{ Math.round(e.temps_depuis_precedent_min) }} min</span>
        </li>
      </ol>
    </div>

    <div v-if="comparaisons.length > 0" class="bg-white shadow rounded-lg p-6">
      <h3 class="text-lg font-semibold mb-4">Comparaison des 3 stratégies</h3>
      <div class="grid grid-cols-3 gap-4">
        <div v-for="r in comparaisons" :key="r.strategie_utilisee" class="border rounded p-4">
          <h4 class="font-semibold text-indigo-600 mb-2">{{ r.strategie_utilisee }}</h4>
          <div class="space-y-1 text-sm">
            <div><span class="text-gray-500">Distance :</span> <span class="font-medium">{{ r.distance_totale_km.toFixed(1) }} km</span></div>
            <div><span class="text-gray-500">Temps :</span> <span class="font-medium">{{ Math.round(r.temps_total_minutes) }} min</span></div>
            <div><span class="text-gray-500">Charge :</span> <span class="font-medium">{{ (r.charge_moyenne * 100).toFixed(0) }}%</span></div>
          </div>
          <div class="mt-3 text-xs text-gray-500">
            <div v-for="e in r.etapes" :key="e.ordre">{{ e.ordre }}. {{ e.nom_lieu }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
