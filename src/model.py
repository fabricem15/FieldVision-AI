import tensorflow as tf

class Model:
    def __init__(self, model_save_path):
        self.model_path = model_save_path
        self.model = None

        self.model = tf.keras.models.load_model(model_save_path, custom_objects={'outfielder_positioning_loss': self.outfielder_positioning_loss})
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)

        self.model.compile(optimizer=optimizer, loss=self.outfielder_positioning_loss, metrics=['accuracy'])

    def outfielder_positioning_loss(y_true, y_pred, grid_size=125, lambda_dist=0.1, lambda_reg=1e-4):
        """
        Improved loss function combining CCE, a distance penalty, and regularization.

        Args:
            y_true: One-hot encoded vector of ball landing position (batch_size, grid_size * grid_size)
            y_pred: Predicted heatmap (batch_size, grid_size * grid_size)
            grid_size: Size of the grid
            lambda_dist: Weighting factor for the distance penalty
            lambda_reg: Regularization weight for confidence penalty

        Returns:
            The combined loss.
        """
        # 1. Calculate CCE Loss
        cce_loss = tf.keras.losses.CategoricalCrossentropy()(y_true, y_pred)

        # 2. Convert Predictions to Coordinates
        num_fielders = 9  # Number of fielders
        top_probs, top_indices = tf.math.top_k(y_pred, k=num_fielders)  # (batch_size, num_fielders)
        top_row_indices = tf.math.floordiv(top_indices, grid_size)
        top_col_indices = tf.math.floormod(top_indices, grid_size)
        top_coords = tf.stack([tf.cast(top_col_indices, tf.float32), tf.cast(top_row_indices, tf.float32)], axis=-1)

        # 3. True Landing Spot Coordinates
        true_indices = tf.argmax(y_true, axis=-1)
        true_row_indices = tf.cast(tf.math.floordiv(true_indices, grid_size), tf.float32)
        true_col_indices = tf.cast(tf.math.floormod(true_indices, grid_size), tf.float32)
        true_coords = tf.stack([true_col_indices, true_row_indices], axis=-1)  # (batch_size, 2)

        # 4. Distance Penalty
        # Compute distances between top predictions and true coordinates
        true_coords_expanded = tf.expand_dims(true_coords, axis=1)  # (batch_size, 1, 2)
        distances = tf.norm(top_coords - true_coords_expanded, axis=-1)  # (batch_size, num_fielders)
        min_distances = tf.reduce_min(distances, axis=-1)  # Closest distance per batch
        distance_penalty = tf.reduce_mean(min_distances)  # Average over batch

        # 5. Confidence Regularization
        reg_penalty = tf.reduce_mean(tf.square(top_probs - 1))  # Penalize under-confident predictions
        
        # 6. Combine Losses
        combined_loss = cce_loss + lambda_dist * distance_penalty + lambda_reg * reg_penalty

        return combined_loss

    def get_model(self):
        if self.model is None:
            print("Model is not loaded yet. Call load_model() first.")
        return self.model