# E-Shop Checkout - Product Specifications

## Version: 1.0
## Last Updated: November 2025

---

## Product Catalog

### Available Products

1. **Wireless Headphones**
   - Product ID: product1
   - Price: $99.99
   - Description: Premium noise-canceling headphones
   - Features: Wireless connectivity, noise cancellation

2. **Smart Watch**
   - Product ID: product2
   - Price: $149.99
   - Description: Fitness tracker with heart monitor
   - Features: Heart rate monitoring, step tracking, notifications

3. **Bluetooth Speaker**
   - Product ID: product3
   - Price: $79.99
   - Description: Portable waterproof speaker
   - Features: Bluetooth 5.0, waterproof (IPX7), 12-hour battery life

---

## Shopping Cart Features

### Cart Management
- Users can add products to cart by clicking "Add to Cart" button
- Each product can be added multiple times (quantity increases)
- Cart displays: product name, unit price, quantity, and line total
- Users can modify quantity using the quantity input field
- Setting quantity to 0 removes the item from cart
- Cart shows a total price that updates dynamically

### Cart Calculations
- Subtotal = Sum of (product price × quantity) for all items
- Final total includes subtotal + shipping - discount

---

## Discount Code System

### Valid Discount Codes

1. **SAVE15**
   - Discount: 15% off the subtotal
   - Applied to cart subtotal only (before shipping)
   - Cannot be combined with other discounts

2. **SAVE10**
   - Discount: 10% off the subtotal
   - Applied to cart subtotal only (before shipping)
   - Cannot be combined with other discounts

### Discount Rules
- Only one discount code can be applied per order
- Discount codes are case-insensitive (SAVE15 = save15 = SaVe15)
- Invalid codes show error message: "Invalid discount code"
- Empty discount code shows: "Please enter a discount code"
- Discount is applied before shipping costs are added
- Discount success message: "X% discount applied!" (where X is the percentage)

---

## Shipping Options

### Standard Shipping
- Cost: **Free** ($0.00)
- Default selection
- Radio button ID: shipping-standard
- Value: "standard"

### Express Shipping
- Cost: **$10.00** (flat rate)
- Radio button ID: shipping-express
- Value: "express"
- Added to final total after discount is applied

### Shipping Calculation Rules
- Shipping cost is added to the final total
- Shipping is calculated after discount is applied
- Only one shipping method can be selected at a time

---

## Payment Methods

### Available Payment Methods

1. **Credit Card**
   - Radio button ID: payment-credit
   - Value: "credit_card"
   - Default selection

2. **PayPal**
   - Radio button ID: payment-paypal
   - Value: "paypal"

### Payment Rules
- One payment method must be selected
- Payment method selection is required before checkout

---

## Form Validation Rules

### Required Fields
All fields marked with asterisk (*) are mandatory:

1. **Full Name**
   - Field ID: customer-name
   - Validation: Cannot be empty
   - Error message: "Name is required"
   - Error displayed in red text below field

2. **Email Address**
   - Field ID: customer-email
   - Validation: Must be valid email format (contains @ and domain)
   - Error message: "Please enter a valid email address"
   - Error displayed in red text below field
   - Email regex: Must match pattern `[text]@[domain].[extension]`

3. **Shipping Address**
   - Field ID: customer-address
   - Validation: Cannot be empty
   - Error message: "Address is required"
   - Error displayed in red text below field

### Additional Validation
- Cart cannot be empty during checkout
- If cart is empty, alert message: "Your cart is empty. Please add items before checkout."

---

## Checkout Process

### Payment Flow
1. User fills in all required form fields
2. User selects shipping method (Standard or Express)
3. User selects payment method (Credit Card or PayPal)
4. User clicks "Pay Now" button (ID: pay-now)
5. System validates all form fields
6. If validation passes:
   - Success message is displayed: "Payment Successful!"
   - Form is hidden
   - Success message shown in green background
7. If validation fails:
   - Appropriate error messages displayed in red below each invalid field
   - Form remains visible for correction

### Success Criteria
- All required fields must be filled
- Email must be in valid format
- Cart must contain at least one item
- Shipping method must be selected
- Payment method must be selected

---

## Price Calculation Examples

### Example 1: Basic Order
- Wireless Headphones × 1 = $99.99
- Shipping: Standard (Free)
- Discount: None
- **Total: $99.99**

### Example 2: Order with Discount
- Smart Watch × 1 = $149.99
- Discount: SAVE15 (15% off)
- Subtotal after discount: $127.49
- Shipping: Standard (Free)
- **Total: $127.49**

### Example 3: Order with Express Shipping
- Bluetooth Speaker × 2 = $159.98
- Discount: None
- Shipping: Express ($10.00)
- **Total: $169.98**

### Example 4: Complete Order
- Wireless Headphones × 1 = $99.99
- Smart Watch × 1 = $149.99
- Subtotal: $249.98
- Discount: SAVE15 (15% off) = -$37.50
- Subtotal after discount: $212.48
- Shipping: Express ($10.00)
- **Total: $222.48**

---

## Error Handling

### Form Errors
- All validation errors are displayed inline below the respective field
- Error text color: Red (#FF0000)
- Errors appear immediately upon form submission if validation fails
- Errors disappear when field is corrected

### Cart Errors
- Empty cart prevents checkout
- Alert message displayed if user attempts checkout with empty cart

### Discount Errors
- Invalid discount codes show error in discount section
- Error remains visible until valid code entered or field cleared
