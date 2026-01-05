// Enhanced Tinder-like swipe functionality for Latagan

class SwipeCard {
    constructor() {
        this.currentIndex = 0;
        this.cards = [];
        this.startX = 0;
        this.startY = 0;
        this.currentX = 0;
        this.isDragging = false;
        this.isAnimating = false;
        this.threshold = window.innerWidth * 0.08; // Very sensitive threshold - only 8% of viewport
        this.init();
    }

    init() {
        const cardContainer = document.getElementById('swipe-card-stack');
        if (!cardContainer) return;

        this.cards = Array.from(document.querySelectorAll('.swipe-card'));
        if (this.cards.length === 0) return;

        this.setupEventListeners();
        this.updateCardPositions();
        this.setupButtonControls();
        
        // Expose globally for button controls
        window.swiper = this;
    }

    setupEventListeners() {
        // Touch events
        document.addEventListener('touchstart', (e) => this.handleStart(e), false);
        document.addEventListener('touchmove', (e) => this.handleMove(e), { passive: false });
        document.addEventListener('touchend', (e) => this.handleEnd(e), false);
        
        // Mouse events
        document.addEventListener('mousedown', (e) => this.handleStart(e), false);
        document.addEventListener('mousemove', (e) => this.handleMove(e), false);
        document.addEventListener('mouseup', (e) => this.handleEnd(e), false);
    }

    setupButtonControls() {
        const nopeBtn = document.getElementById('nope-btn');
        const addBtn = document.getElementById('add-btn');
        
        if (nopeBtn) nopeBtn.addEventListener('click', () => this.handleNopeClick());
        if (addBtn) addBtn.addEventListener('click', () => this.handleAddClick());
    }

    handleStart(e) {
        if (this.isAnimating) return;
        
        const card = e.target.closest('.swipe-card');
        if (!card || !card.classList.contains('active')) return;
        
        this.isDragging = true;
        this.startX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
        this.startY = e.type.includes('touch') ? e.touches[0].clientY : e.clientY;
        this.currentX = this.startX;
        
        // Remove transition for smooth dragging
        card.style.transition = 'none';
        card.style.cursor = 'grabbing';
    }

    handleMove(e) {
        if (!this.isDragging || this.isAnimating) return;
        
        const card = this.cards[this.currentIndex];
        if (!card) return;

        const currentX = e.type.includes('touch') ? e.touches[0].clientX : e.clientX;
        const currentY = e.type.includes('touch') ? e.touches[0].clientY : e.clientY;
        const diffX = currentX - this.startX;
        const diffY = currentY - this.startY;
        
        // Only process horizontal swipes
        if (Math.abs(diffX) <= Math.abs(diffY)) return;
        
        e.preventDefault();
        this.currentX = currentX;

        // Set tight boundary for drag (closer to edge for falling effect)
        const maxDrag = window.innerWidth * 0.35;
        const constrainedDiffX = Math.max(-maxDrag, Math.min(maxDrag, diffX));

        // Calculate rotation and opacity based on drag distance
        const dragPercent = constrainedDiffX / window.innerWidth;
        const rotate = dragPercent * 30;
        const opacity = Math.max(0.4, 1 - Math.abs(dragPercent) * 0.6);
        
        card.style.transform = `translateX(${constrainedDiffX}px) rotate(${rotate}deg)`;
        card.style.opacity = opacity;

        // Add visual feedback for swipe direction
        card.classList.remove('swiped-left', 'swiped-right');
        if (Math.abs(constrainedDiffX) > 50) {
            if (constrainedDiffX > 0) {
                card.classList.add('swiped-right');
            } else {
                card.classList.add('swiped-left');
            }
        }
    }

    handleEnd(e) {
        if (!this.isDragging || this.isAnimating) return;
        
        this.isDragging = false;
        const card = this.cards[this.currentIndex];
        if (!card) return;
        
        card.style.cursor = 'grab';

        // Apply same constraint as handleMove for consistency
        const maxDrag = window.innerWidth * 0.35;
        const diffX = Math.max(-maxDrag, Math.min(maxDrag, this.currentX - this.startX));
        
        // Determine if swipe was far enough
        if (Math.abs(diffX) > this.threshold) {
            if (diffX > 0) {
                this.swipeRight(card);
            } else {
                this.swipeLeft(card);
            }
        } else {
            // Snap back to center
            this.resetCard(card);
        }
    }

    resetCard(card) {
        card.style.transition = 'all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
        card.style.transform = 'translateX(0) rotate(0)';
        card.style.opacity = '1';
        card.classList.remove('swiped-right', 'swiped-left');
    }

    swipeRight(card) {
        this.isAnimating = true;
        const itemId = card.dataset.itemId;
        
        // Falling animation to the right
        card.style.transition = 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        card.style.transform = `translateX(${window.innerWidth * 2}px) rotate(30deg) translateY(100px)`;
        card.style.opacity = '0';

        // Add to cart via AJAX
        setTimeout(() => {
            if (itemId) {
                // Get CSRF token from the page
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
                
                const formData = new FormData();
                formData.append('csrfmiddlewaretoken', csrfToken);
                
                fetch(`/cart/add/${itemId}/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.success) {
                        // Show toast notification
                        this.showToast(data.message);
                    } else {
                        this.showToast(data.error || 'Error adding to cart', 'error');
                    }
                })
                .catch(error => {
                    console.error('Error adding to cart:', error);
                    this.showToast('Error adding to cart', 'error');
                });
            }
            
            this.currentIndex++;
            this.moveToNextCard();
        }, 600);
    }

    swipeLeft(card) {
        this.isAnimating = true;
        
        // Falling animation to the left
        card.style.transition = 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
        card.style.transform = `translateX(-${window.innerWidth * 2}px) rotate(-30deg) translateY(100px)`;
        card.style.opacity = '0';

        setTimeout(() => {
            this.moveToNextCard();
        }, 600);
    }

    moveToNextCard() {
        const currentCard = this.cards[this.currentIndex];
        if (currentCard) {
            currentCard.remove();
        }
        
        this.cards = this.cards.filter((_, i) => i !== this.currentIndex);
        
        if (this.cards.length > 0) {
            this.isAnimating = false;
            this.updateCardPositions();
        } else {
            this.showEndMessage();
        }
    }

    updateCardPositions() {
        this.cards.forEach((card, index) => {
            if (index === this.currentIndex) {
                card.classList.add('active');
                // Add slight scale on active card for depth effect
                card.style.transform = 'scale(1)';
            } else {
                card.classList.remove('active');
            }
        });
    }

    handleNopeClick() {
        const card = this.cards[this.currentIndex];
        if (card && !this.isAnimating) {
            this.swipeLeft(card);
        }
    }

    handleAddClick() {
        const card = this.cards[this.currentIndex];
        if (card && !this.isAnimating) {
            this.swipeRight(card);
        }
    }

    showEndMessage() {
        this.isAnimating = false;
        const container = document.getElementById('swipe-card-stack');
        container.innerHTML = `
            <div style="
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 500px;
                background: linear-gradient(135deg, #1a2d4d 0%, #2d4a73 100%);
                border-radius: 12px;
                color: white;
                text-align: center;
                animation: slideUp 0.5s ease-out;
            ">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
                <h2 style="font-size: 2rem; margin: 0.5rem 0; color: white;">All Done!</h2>
                <p style="font-size: 1.1rem; margin: 1rem 0 2rem 0; color: #ccc; max-width: 300px;">You've explored all available items</p>
                <a href="/browse/" class="btn btn-primary" style="padding: 0.8rem 2rem; font-size: 1rem;">Browse More Items</a>
            </div>
            <style>
                @keyframes slideUp {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            </style>
        `;
    }

    showToast(message, type = 'success') {
        // Create toast element
        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'success' ? '#51cf66' : '#ff6b6b'};
            color: white;
            border-radius: 4px;
            font-weight: 600;
            z-index: 9999;
            animation: slideIn 0.3s ease-out;
            max-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        `;
        toast.textContent = message;
        document.body.appendChild(toast);

        // Add animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { 
                    opacity: 0; 
                    transform: translateX(400px);
                }
                to { 
                    opacity: 1; 
                    transform: translateX(0);
                }
            }
            @keyframes slideOut {
                from { 
                    opacity: 1; 
                    transform: translateX(0);
                }
                to { 
                    opacity: 0; 
                    transform: translateX(400px);
                }
            }
        `;
        document.head.appendChild(style);

        // Remove after 3 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const cardStack = document.getElementById('swipe-card-stack');
    if (cardStack && document.querySelectorAll('.swipe-card').length > 0) {
        new SwipeCard();
    }
});
