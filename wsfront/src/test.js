
        let wastes = [];
        let events = [];
        let campaigns = [];
        let currentPage = 'home';

        function showPage(pageName) {
            document.querySelectorAll('.page-content').forEach(page => {
                page.classList.add('hidden');
            });
            
            const pageMap = {
                'home': 'home-page',
                'add-waste': 'add-waste-page',
                'waste-list': 'waste-list-page',
                'waste-types': 'waste-types-page',
                'centers': 'centers-page',
                'users': 'users-page',
                'equipment': 'equipment-page',
                'events': 'events-page',
                'add-event': 'add-event-page',
                'add-campaign': 'add-campaign-page',
                'dashboard': 'dashboard-page'
            };
            
            const pageId = pageMap[pageName];
            if (pageId) {
                document.getElementById(pageId).classList.remove('hidden');
                currentPage = pageName;
                
                if (pageName === 'waste-list') {
                    renderWasteTable();
                }
            }
            
            const mobileMenu = document.getElementById('mobile-menu');
            if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('hidden');
            }
            
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function toggleMenu() {
            const mobileMenu = document.getElementById('mobile-menu');
            mobileMenu.classList.toggle('hidden');
        }

        document.getElementById('waste-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const waste = {
                id: Date.now(),
                type: document.getElementById('waste-type').value,
                weight: document.getElementById('waste-weight').value,
                location: document.getElementById('waste-location').value,
                description: document.getElementById('waste-description').value,
                date: document.getElementById('waste-date').value,
                status: document.getElementById('waste-status').value
            };
            
            wastes.push(waste);
            
            this.reset();
            
            showNotification('Déchet ajouté avec succès!');
            
            setTimeout(() => {
                showPage('waste-list');
            }, 1500);
        });

        document.getElementById('event-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const event = {
                id: Date.now(),
                title: document.getElementById('event-title').value,
                type: document.getElementById('event-type').value,
                description: document.getElementById('event-description').value,
                date: document.getElementById('event-date').value,
                time: document.getElementById('event-time').value,
                location: document.getElementById('event-location').value,
                capacity: document.getElementById('event-capacity').value,
                organizer: document.getElementById('event-organizer').value,
                contact: document.getElementById('event-contact').value,
                objectives: document.getElementById('event-objectives').value,
                participants: 0,
                status: 'planifie'
            };
            
            events.push(event);
            
            this.reset();
            
            showNotification('Événement créé avec succès!');
            
            setTimeout(() => {
                showPage('events');
            }, 1500);
        });

        document.getElementById('campaign-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const campaign = {
                id: Date.now(),
                title: document.getElementById('campaign-title').value,
                type: document.getElementById('campaign-type').value,
                description: document.getElementById('campaign-description').value,
                startDate: document.getElementById('campaign-start-date').value,
                endDate: document.getElementById('campaign-end-date').value,
                target: document.getElementById('campaign-target').value,
                goalType: document.getElementById('campaign-goal-type').value,
                goalValue: document.getElementById('campaign-goal-value').value,
                budget: document.getElementById('campaign-budget').value,
                actions: document.getElementById('campaign-actions').value,
                coordinator: document.getElementById('campaign-coordinator').value,
                contact: document.getElementById('campaign-contact').value,
                progress: 0,
                participants: 0,
                status: 'active'
            };
            
            campaigns.push(campaign);
            
            this.reset();
            
            showNotification('Campagne lancée avec succès!');
            
            setTimeout(() => {
                showPage('events');
            }, 1500);
        });

        function renderWasteTable() {
            const tbody = document.getElementById('waste-table-body');
            
            if (wastes.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                            <div class="text-6xl mb-4">📦</div>
                            <p class="text-lg font-semibold">Aucun déchet enregistré</p>
                            <p class="text-sm mt-2">Commencez par ajouter votre premier déchet</p>
                        </td>
                    </tr>
                `;
                return;
            }
            
            tbody.innerHTML = wastes.map(waste => {
                const statusColors = {
                    'en-attente': 'bg-yellow-100 text-yellow-700',
                    'collecte': 'bg-blue-100 text-blue-700',
                    'traite': 'bg-purple-100 text-purple-700',
                    'recycle': 'bg-green-100 text-green-700'
                };
                
                const statusLabels = {
                    'en-attente': 'En Attente',
                    'collecte': 'En Collecte',
                    'traite': 'Traité',
                    'recycle': 'Recyclé'
                };
                
                const typeIcons = {
                    'plastique': '🥤',
                    'verre': '🍾',
                    'papier': '📄',
                    'metal': '🥫',
                    'organique': '🍎',
                    'electronique': '💻',
                    'dangereux': '⚠️'
                };
                
                return `
                    <tr class="hover:bg-emerald-50 transition">
                        <td class="px-6 py-4">
                            <div class="flex items-center space-x-2">
                                <span class="text-2xl">${typeIcons[waste.type] || '📦'}</span>
                                <span class="font-semibold text-gray-800 capitalize">${waste.type}</span>
                            </div>
                        </td>
                        <td class="px-6 py-4 text-gray-700">${waste.weight} kg</td>
                        <td class="px-6 py-4 text-gray-700">${waste.location}</td>
                        <td class="px-6 py-4 text-gray-700">${waste.date}</td>
                        <td class="px-6 py-4">
                            <span class="px-3 py-1 rounded-full text-sm font-semibold ${statusColors[waste.status]}">
                                ${statusLabels[waste.status]}
                            </span>
                        </td>
                        <td class="px-6 py-4">
                            <button onclick="deleteWaste(${waste.id})" class="text-red-600 hover:text-red-800 font-semibold">
                                Supprimer
                            </button>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function deleteWaste(id) {
            const wasteIndex = wastes.findIndex(w => w.id === id);
            if (wasteIndex === -1) return;
            
            const confirmDiv = document.createElement('div');
            confirmDiv.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
            confirmDiv.innerHTML = `
                <div class="bg-white rounded-2xl p-8 max-w-md mx-4 shadow-2xl">
                    <h3 class="text-2xl font-bold text-gray-800 mb-4">Confirmer la suppression</h3>
                    <p class="text-gray-600 mb-6">Êtes-vous sûr de vouloir supprimer ce déchet ?</p>
                    <div class="flex space-x-4">
                        <button onclick="this.closest('.fixed').remove()" class="flex-1 bg-gray-200 text-gray-700 py-3 rounded-xl font-semibold hover:bg-gray-300 transition">
                            Annuler
                        </button>
                        <button onclick="confirmDelete(${id}); this.closest('.fixed').remove();" class="flex-1 bg-red-500 text-white py-3 rounded-xl font-semibold hover:bg-red-600 transition">
                            Supprimer
                        </button>
                    </div>
                </div>
            `;
            document.body.appendChild(confirmDiv);
        }

        function confirmDelete(id) {
            wastes = wastes.filter(w => w.id !== id);
            renderWasteTable();
            showNotification('Déchet supprimé avec succès!');
        }

        function showNotification(message) {
            const notification = document.createElement('div');
            notification.className = 'fixed top-24 right-4 bg-emerald-500 text-white px-6 py-4 rounded-xl shadow-2xl z-50 fade-in';
            notification.innerHTML = `
                <div class="flex items-center space-x-3">
                    <span class="text-2xl">✓</span>
                    <span class="font-semibold">${message}</span>
                </div>
            `;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.style.opacity = '0';
                notification.style.transform = 'translateY(-20px)';
                notification.style.transition = 'all 0.3s ease';
                setTimeout(() => notification.remove(), 300);
            }, 3000);
        }

        showPage('home');
 