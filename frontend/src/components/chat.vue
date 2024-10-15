    <template>
        <div class="chat-container">
        <!-- <div v-if="loading">Loading...</div> -->
        <div v-if="isLoadingPartners">Loading partners...</div>
        <div v-else-if="!currentUser">Please log in to use the chat.</div>
        <div v-else-if="!selectedPartner" class="partner-selection">
        <h2>Select a {{ currentUser.userType === 'supplier' ? 'Restaurant' : 'Supplier' }} to chat with:</h2>
        <ul>
            <li v-for="partner in availablePartners" :key="partner.id" @click="selectPartner(partner)">
            {{ partner.name }}
            </li>
        </ul>
        </div>
        <div v-else>
        <h2>Chat with {{ selectedPartner.name }}</h2>
        <div class="messages-container" ref="messagesContainer">
            <ul id="messages">
            <li v-for="message in filteredMessages" :key="message.id" :class="{ 'current-user': message.userId === currentUser.uid }">
                <strong>{{ getUserName(message.userId) }}</strong>: {{ message.text }}
            </li>
            </ul>
        </div>
        <form @submit.prevent="sendMessage" class="message-form">
            <label :for="messageInputId">Type a message:</label>
            <input 
            :id="messageInputId"
            v-model="newMessage" 
            autocomplete="off" 
            placeholder="Type a message..." 
            />
            <button type="submit">Send</button>
        </form>
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-else-if="availablePartners.length === 0">No available partners found.</div>  
        </div>
    </div>
    </template>
    
    <script setup>
    import { ref, computed, onMounted, watch, nextTick } from 'vue';
    import { auth, db } from '../firebase.js';
    import { onAuthStateChanged } from 'firebase/auth';
    import { collection, addDoc, onSnapshot, query, where, orderBy, serverTimestamp, getDoc, doc, getDocs } from 'firebase/firestore';
    
    const currentUser = ref(null);
    const messages = ref([]);
    const newMessage = ref('');
    const error = ref(null);
    const messagesContainer = ref(null);
    const userNames = ref({});
    const selectedPartner = ref(null);
    const availablePartners = ref([]);
    const loading = ref(true);
    const isLoadingPartners = ref(false);
    
    const conversationId = computed(() => {
        if (currentUser.value && selectedPartner.value) {
        return [currentUser.value.uid, selectedPartner.value.id].sort().join('_');
        }
        return null;
    });
    
    const filteredMessages = computed(() => {
        return messages.value.filter(message => 
        message.conversationId === conversationId.value
        );
    });
    
    const sendMessage = async () => {
        error.value = null;
        if (newMessage.value && currentUser.value && selectedPartner.value) {
        try {
            await addDoc(collection(db, 'messages'), {
            text: newMessage.value,
            timestamp: serverTimestamp(),
            userId: currentUser.value.uid,
            conversationId: conversationId.value
            });
            newMessage.value = '';
        } catch (err) {
            console.error("Error sending message: ", err);
            error.value = "Failed to send message: " + err.message;
        }
        } else {
        error.value = newMessage.value ? "Please select a partner to chat with" : "Cannot send empty message";
        }
    };
    
    const loadMessages = () => {
        if (!conversationId.value) return;
    
        const messagesRef = collection(db, 'messages');
        const q = query(
        messagesRef,
        where('conversationId', '==', conversationId.value),
        orderBy('timestamp', 'asc')
        );
    
        onSnapshot(q, (snapshot) => {
        messages.value = snapshot.docs.map(doc => ({
            id: doc.id,
            ...doc.data()
        }));
        
        nextTick(() => {
            scrollToBottom();
        });
    
        messages.value.forEach(message => {
            if (!userNames.value[message.userId]) {
            fetchUserName(message.userId);
            }
        });
        }, (err) => {
        console.error("Error loading messages: ", err);
        error.value = "Failed to load messages: " + err.message;
        });
    };
    
    const fetchUserName = async (userId) => {
        try {
        const userDoc = await getDoc(doc(db, 'users', userId));
        if (userDoc.exists()) {
            const userData = userDoc.data();
            userNames.value[userId] = userData.username || 'Unknown User';
        } else {
            userNames.value[userId] = 'Unknown User';
        }
        } catch (err) {
        console.error("Error fetching username: ", err);
        userNames.value[userId] = 'Unknown User';
        }
    };
    
    const getUserName = (userId) => {
        return userNames.value[userId] || 'Loading...';
    };
    
    const selectPartner = (partner) => {
        selectedPartner.value = partner;
        loadMessages();
    };
    
    onMounted(() => {
    console.log("Component mounted");
    onAuthStateChanged(auth, async (user) => {
        console.log("Auth state changed. User:", user);
        loading.value = true;
        if (user) {
            console.log("User is authenticated. UID:", user.uid);
            try {
                const userDocRef = doc(db, 'users', user.uid);
                const userDoc = await getDoc(userDocRef);
                if (userDoc.exists()) {
                    currentUser.value = { 
                        uid: user.uid, 
                        userName: userDoc.data().userName,
                        userType: userDoc.data().userType
                    };
                    console.log("Current user set:", currentUser.value);
                    loadAvailablePartners();
                } else {
                    console.error('User document not found in Firestore');
                    currentUser.value = null;
                }
            } catch (error) {
                console.error('Error fetching user document:', error);
                currentUser.value = null;
            }
        } else {
            console.log("No authenticated user");
            currentUser.value = null;
        }
        loading.value = false;
    });
});

    const loadAvailablePartners = async () => {
        if (!currentUser.value) return;

        isLoadingPartners.value = true;
        const usersRef = collection(db, 'users');
        const partnerType = currentUser.value.userType === 'restaurant' ? 'supplier' : 'restaurant';
        // console.log(partnerType);
        const q = query(usersRef, where('userType', '==', partnerType), orderBy('userName'))

        try {
            const snapshot = await getDocs(q);
            availablePartners.value = snapshot.docs.map(doc => ({
            id: doc.id,
            userName: doc.data().userName,
            userType: doc.data().userType,
            }));
        console.log("Available partners:", availablePartners.value);
        } catch (err) {
            console.error("Error loading partners:", err);
            error.value = "Failed to load partners: " + err.message;
        } finally {
        isLoadingPartners.value = false;
        }
        };
    const messageInputId = 'message-input';
    </script>

    
    
    <style scoped>
    
    .partner-selection {
        padding: 1rem;
    }
    
    .partner-selection ul {
        list-style-type: none;
        padding: 0;
    }
    
    .partner-selection li {
        cursor: pointer;
        padding: 0.5rem;
        margin-bottom: 0.5rem;
        background-color: #f0f0f0;
        border-radius: 4px;
    }
    
    .partner-selection li:hover {
        background-color: #e0e0e0;
    }
    
    #messages li:not(.current-user) {
        background-color: white;
        border-radius: 18px 18px 18px 0;
        float: left;
        text-align: left;
    }
    
    #messages li.current-user {
        background-color: #e6f3ff;
        border-radius: 18px 18px 0 18px;
        float: right;
        text-align: right;
    }
    label {
    display: block;
    margin-bottom: 5px;
    }

    .message-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    }

    .message-form input {
    flex-grow: 1;
    }

    .message-form button {
    align-self: flex-end;
    }
    </style>